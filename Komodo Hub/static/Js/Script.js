
// TROY KENNETH MUYOBO CODE

async function getAvatar(choice){

    if (choice == undefined){
     let OG = 'lorelei';
     const Data = await fetch(`https://api.dicebear.com/9.x/${OG}/svg`)
     const DATAJSON = await Data.text()
     const AvatarDiv = document.querySelector('.Avatar-Image')
     AvatarDiv.innerHTML = `${DATAJSON}`
     console.log("Yes")
    }
    else if (choice){
      console.log(choice)
      const Data = await fetch(`https://api.dicebear.com/9.x/${choice}/svg`)
      const DATAJSON = await Data.text()
      const AvatarDiv = document.querySelector('.Avatar-Image')
      AvatarDiv.innerHTML = `${DATAJSON}`
      console.log("Yes")
      POST_AVATAR(choice)
    }
  }
  function isValidUsername(username) { /// Helper function to validate username 
      const alphanumericRegex = /^[a-zA-Z0-9]+$/;
      if(username.length > 3 && alphanumericRegex.test(username)){
          return true
      }
      else{
          
          return false
      }
  }
  
  function IsValidDescription(description){
      const alphanumericRegex = /^[a-zA-Z0-9]+$/;
      if(description.length  <= 40 && description.length > 0)
          {
          return true 
      }
      else{
          return false
      }
  }
  async function ChangeYourUserName(){
      try {
      const Data = document.querySelector(".Change-Username").value
      if(isValidUsername(Data)){
      const response = await fetch('/Change_Username', {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({ 'NewUsername': Data }) // Ensure correct key "avatar"
      });
      console.log("Hello")
  }
  else{
      alert('Username can not contain symbols')
  }
  }
  catch(error){
      console.log(error)
  }
  }
  async function RetrieveAvatar(){
      try{
          const data = await fetch('/get_avatar')
          const dataJSON = await data.json()
          const Final = dataJSON.AvatarChoice
          getAvatar(Final)
      }
      
      catch(error){
          console.log(error)
      }
  }
  async function POST_AVATAR(choice) {
      try {
          const response = await fetch('/set_avatar', {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify({ 'avatar': choice }) // Ensure correct key "avatar"
          });
  
          if (!response.ok) {
              throw new Error(`Server error: ${response.status}`);
          }
          console.log("Success, server side");
      } catch (error) {
          console.error("Error:", error);
      }
  }
  document.addEventListener("DOMContentLoaded", function() {
    const button = document.querySelector(".Description-button")
    button.addEventListener("click", POSTUserInput);
    const ChangeYourProfileButton = document.querySelector(".Change-input-button")
    ChangeYourProfileButton.addEventListener("click",ChangeYourUserName)
    // Fetch the profile description when the page is loaded
    GetProfileDescription()
    RetrieveAvatar()
  })
  
  async function GetProfileDescription(){
      try{
      const data = await fetch("/get_profile_description")
      const dataJSON = await data.json()
      if(dataJSON.description != null ){
          console.log(dataJSON.description)
      document.querySelector(".Description-Container").innerHTML = `<div class="Finished-Description"><h1 class="Description-text">${dataJSON.description}</h1> </div>` }
       }
      catch(error){
          console.log(error)
  
      }
  }
  async function POSTUserInput(){
      UserInput = document.querySelector(".Description-text-box")
  
      const newDescription = UserInput.value;
  
      if (!IsValidDescription(newDescription)) {
          alert('Invalid description, cannot contain non-alphanumeric characters ')
  
                 }
      else{
         try { 
          POSTData =  await fetch("/update_description", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
              },
              body: JSON.stringify({ description: newDescription }),
          })
          await console.log(POSTData)
          console.log('Success')
          console.log(newDescription)
          document.querySelector(".Description-Container").innerHTML = `<h1>${newDescription}</h1>`
      }
      catch(error){
          console.log(error)
      }
      }
      
  }