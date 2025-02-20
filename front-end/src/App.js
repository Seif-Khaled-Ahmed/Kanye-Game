import "./App.css";
import image1 from "./images/output_35.png";
import Counter from "./Animations/Counter/Counter.jsx";

function App() {
  return (
    <div id="big-big-container">
      <div id="left-container">
        <div id="container">
          <div id="image">
            <img src={image1} alt="Example "></img>
          </div>
        </div>
      </div>
      <div id="right-container">
        <div id="score">
          <p>Score</p>
          <Counter
            value={100}
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
