# python_scripting_supervision

It's a programm dedictaed to monitoring several parts of my labtop and get the datas out of into a text file and then into a SQl database (workbench) and upload these datas into a data vizualisation tool which allow me to have an overview of my labtop state in real time through graphics. 

ressources :
  - python (PyCharm)
  - PSUTIL library -> grab the functions related to each element i want to monitor  
  - time library -> to create a refresh process to upload new bashes of datas every 10 seconds 
  - datetime library -> to time stamp every upload of datas into the text file .txt
  - mariadb connector -> to be able to link the program to my sql database
  - Grafana -> data vizualisation tool
  
  <img src="https://cloud.githubusercontent.com/assets/4307137/10105283/251b6868-63ae-11e5-9918-b789d9d682ec.png" width="15%"></img> 
  
  ![Image of Yaktocat](photo-graphique-grafana.png)


