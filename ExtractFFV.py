#import required libraries
import os

import cv2
import numpy as np
from imgbeddings import imgbeddings
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.http import models
import torch


def detect_face(image_path,target_path):
    # loading the haar case algorithm file into alg variable
    alg = "haarcascade_frontalface_default.xml"
    # loading the image path into file_name variable
    file_name = image_path
    # reading the image
    img = cv2.imread(file_name, 0)
    # creating a black and white version of the image
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # passing the algorithm to OpenCV
    haar_cascade = cv2.CascadeClassifier(alg)
    # detecting the faces
    faces = haar_cascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=2, minSize=(90, 90))
    # for each face detected
    for x, y, w, h in faces:
        # crop the image to select only the face
        cropped_image = img[y : y + h, x : x + w]
        # loading the target image path into target_file_name variable
        target_file_name = target_path
        cv2.imwrite(
            target_file_name,
            cropped_image,
        )

def generate_embeddings(image_path):
    #
    # loading the face image path into file_name variable
    file_name = image_path
    # opening the image
    img = Image.open(file_name)
    # loading the `imgbeddings`
    ibed = imgbeddings()
    # calculating the embeddings
    embedding = ibed.to_embeddings(img)[0]
    emb_array = np.array(embedding).reshape(1,-1)
    return emb_array

if __name__ == '__main__':
    # loop through the images in the photos folder and extract faces
    file_path = "frames/s01c01.mp4"
    for item in os.listdir(file_path):
        if item.endswith(".jpeg"):
            detect_face(os.path.join(file_path,item),os.path.join("target",item))

    img_embeddings = [generate_embeddings(os.path.join("target",item)) for item in os.listdir("target")]
    print(len(img_embeddings))
    #
    print(img_embeddings[0].shape)
    #
    #save the vector of embeddings as a NumPy array so that we don't have to run it again later
    np.save("vectors_cv2", np.array(img_embeddings), allow_pickle=False)

    # Create a local Qdrant vector store
    client =QdrantClient(path="qdrant_db_cv2")
    #
    my_collection = "image_collection_cv2"
    client.recreate_collection(
        collection_name=my_collection,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
    )
    # generate metadata
    payload = []
    files_list= os.listdir("target")
    for i in range(len(os.listdir("target"))):
        payload.append({"image_id" :i,
                        "name":files_list[i].split(".")[0]})

    print(payload[:3])
    ids = list(range(len(os.listdir("target"))))
    #Load the embeddings from the save pickle file
    embeddings = np.load("vectors_cv2.npy").tolist()
    #
    # Load the image embeddings
    for i in range(0, len(os.listdir("target"))):
        client.upsert(
            collection_name=my_collection,
            points=models.Batch(
                ids=[ids[i]],
                vectors=embeddings[i],
                payloads=[payload[i]]
            )
        )


    client.count(
        collection_name=my_collection,
        exact=True,
    )

    client.scroll(
        collection_name=my_collection,
        limit=10
    )