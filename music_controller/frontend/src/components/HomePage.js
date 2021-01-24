import React, { Component } from 'react';
// We don't need to import render because in App.js we are rendering the App component 
// Render the homepage component from the App component
// Let's import the RoomJoinPage component
import RoomJoinPage from "./RoomJoinPage";
// Let's import the CreateRoomPage component
import CreateRoomPage from "./CreateRoomPage";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";

// From this component we do the routing system

export default class HomePage extends Component{
    constructor(props){
        // Call the constructor of component which is necessary
        super(props);
    }
    // Switch works the same as in other coding languages 
    // We use it for routing purposes
    // Whenever we add a new page we need to add it to Django and React
    render(){
        return (
            <Router>
                <Switch>
                    <Route exact path="/"><p>This is the homepage</p></Route>
                    <Route path="/join" component={RoomJoinPage}/>
                    <Route path="/create" component={CreateRoomPage}/>
                </Switch>
            </Router>);
    }
}
