# vidar_decrypt_strings
Ghidra Python script do decrypt strings in Vidar samples

If you want to try it out you can grab the used sample from Tria.ge here: https://tria.ge/230302-sq9zysda8v

# How to find the function which starts the decryption for all strings

- In Ghidra, click on Window -> Defined Strings
- Scroll through the list of strings and you'll notice A LOT of those kind of strings:
![image](https://user-images.githubusercontent.com/9799160/222473356-beaf3f0f-d1af-4db2-a9d9-6e5c8351480d.png)
- Right click on one of those strings in the Listing window and choose "References" > "Show references to Address"
![image](https://user-images.githubusercontent.com/9799160/222473963-cd142e43-b15f-492d-a06a-22c226e7c379.png)
- Double click on the reference and you will get to the function we need:
![image](https://user-images.githubusercontent.com/9799160/222474258-f917c88b-9009-428f-aa81-5220b9559b25.png)
- Take note of the function name which is called repeatedly (in this case func_decrypt_string)
- Open the script manager through "Window" > "Script Manager"
- Click on "New Script"
![image](https://user-images.githubusercontent.com/9799160/222474705-6806350a-5e88-476b-b233-e936f6d0f50e.png)
- Choose Python
![image](https://user-images.githubusercontent.com/9799160/222474779-acae4f96-cd5e-44e3-886d-3f5043b5a9b4.png)
- Paste in the content of main.py from this repository
- Replace "func_decrypt_string" with the actual name of the decrypt function you took note of earlier
![image](https://user-images.githubusercontent.com/9799160/222475371-c735656c-3b2b-4a83-8479-0b0af685f101.png)
- Run the script and you will see that the Listing gets populated with comments of the decrypted names:
![image](https://user-images.githubusercontent.com/9799160/222475807-8ea1eca3-f98a-46d3-b224-d72b9c5da3b9.png)

