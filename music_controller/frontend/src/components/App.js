import React, { Component } from "react";
import { render } from "react-dom";
// Let's import the Homepage component
import HomePage from "./HomePage";
// Let's import the RoomJoinPage component
import RoomJoinPage from "./RoomJoinPage";
// Let's import the CreateRoomPage component
import CreateRoomPage from "./CreateRoomPage";

// First component to be render is called App
export default class App extends Component{
    // props is an attribute
    constructor(props){
        super(props);
        // we can write the following state 
        //this.state = {
            // we put stateful aspects that we want to store
            // whenever this state of our component is modified you will automatically re-render the entire component
            // let's say the databse updates and now the website needs to change
            // All we have to do is modify the state of the component and re-render just that component
        //}
    }
    // This method called render will return the html to be display in the page
    render(){
        // render the HomePage, RoomJoinPage and CreateRoomPage components
        // we need to use <div> tags as a wrapper otherwise we would get an error
        return (
            <div>
                <HomePage />
                <RoomJoinPage />
                <CreateRoomPage />
            </div>
            );
    }
}

const appDiv = document.getElementById("app");
// We render the App component into the appDiv in our index.html (the id is "app") placing it
// inside div
// <App /> is the component's tag
// For example, <App name="tim"/> "tim"in this case is a prop inside of the render method we would have:
// return <h1>{this.props.name}</h1>; It needs to be in {} because it's JavaScript inside a html tag
// In this case I will render the string tim or whatever is passed as the name prop to this App component
// We can pass properties to the components and use this properties to meodify its behaviour
render(<App />, appDiv);