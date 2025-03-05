import "./App.css";
import Counter from "./Animations/Counter/Counter.jsx";
import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [imageData, setImageData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const session = async () => {
      const response = await axios.get("http://localhost:3001/");
    };
    const getImage = async () => {
      try {
        const response = await axios.get("http://localhost:3001/image", {
          responseType: "blob",
          withCredentials: true,
        });
        const imageBlob = response.data;
        const imageObjectUrl = URL.createObjectURL(imageBlob); // Create a URL for the blob
        setImageData(imageObjectUrl);
        setLoading(false); // Set loading state to false
      } catch (err) {
        setLoading(false); // Set loading state to false
      }
    };
    // session();
    getImage();
  }, []);

  // useEffect(()=>{
  //   const getRandom = async () =>{
  //     try{
  //       const response = await axios.get("http://localhost:3001/image")
  //     }
  //   }
  // })
  return (
    <div id="big-big-container">
      <div id="left-container">
        <div id="container">
          <div id="image">
            <img src={imageData} alt="Fetched from API" />
          </div>
        </div>
      </div>
      <div id="right-container">
        <div id="score">
          <p>Score</p>
          <Counter
            value={5}
            places={[100, 10, 1]}
            fontSize={80}
            padding={5}
            gap={10}
            textColor="white"
            fontWeight={900}
          />
        </div>
        <div id="choices">
          <div className="choice-div">
            <button className="choice">HI</button>
          </div>
          <div className="choice-div">
            <button className="choice">NIGGERS</button>
          </div>
          <div className="choice-div">
            <button className="choice">Click Me</button>
          </div>
          <div className="choice-div">
            <button className="choice">Click Me</button>
          </div>
          <div className="choice-div">
            <button className="choice">NIGGERS</button>
          </div>
          <div className="choice-div">
            <button className="choice">Click Me</button>
          </div>
          <div className="choice-div">
            <button className="choice">Click Me</button>
          </div>
          <div className="choice-div">
            <button className="choice">Click Me</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
