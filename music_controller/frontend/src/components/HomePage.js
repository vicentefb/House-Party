import React, { Component } from 'react';
// We don't need to import render because in App.js we are rendering the App component 
// Render the homepage component from the App component
// Let's import the RoomJoinPage component
import RoomJoinPage from "./RoomJoinPage";
// Let's import the CreateRoomPage component
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import Info from "./Info";

// From this component we do the routing system

export default class HomePage extends Component{
    constructor(props){
        // Call the constructor of component which is necessary
        super(props);
        this.state = {
            roomCode: null,
        };
        this.clearRoomCode = this.clearRoomCode.bind(this);
    }

    // entry point to know if the user already has an active session
    // In React there are lifecyle methods that let you alter the behaviour of the component
    // componentDidMount is an example of a lifecycle method
    // It means that the component just loaded for the first time in the screen
    // We are going to call an endpoint on the server in an asynchronous manner because it might take some time
    async componentDidMount(){
        // We want to store the room code in the state of the home page
        // We can this the state in our render method as well
        fetch('/api/user-in-room')
        .then((response) => response.json())
        .then((data) => {
            this.setState({
                roomCode: data.code
            });
        });
    }

    // Button Group is to have two buttons horizontally aligned
    renderHomePage(){
        return (
            <Grid container spacing={3}>
                <Grid item xs={12} align="center">
                    <Typography variant="h3" compact="h3">
                        House Party
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <ButtonGroup disableEleveation variant="contained" color="primary">
                        <Button color="primary" to='/join' component={Link}>
                            Join a Room
                        </Button>
                        <Button color="default" to='/info' component={Link}>
                            Info
                        </Button>
                        <Button color="secondary" to='/create' component={Link}>
                            Create a Room
                        </Button>
                    </ButtonGroup>
                </Grid>
            </Grid>
        );
    }

    clearRoomCode(){
        this.setState({
            roomCode: null,
        });
    }

    // Switch works the same as in other coding languages 
    // We use it for routing purposes
    // Whenever we add a new page we need to add it to Django and React
    // The render insde the first Route tag means to call that render function when we are in that page
    /*  props is given by the Route
        the ... is called the spread operator this will take in all of the properties that were passed in
        as the object and kind of spread them out
        leaveRoomCallback is our own prop which is equal to this.clearRoomCode which is a method that we define
        So we are passing a method to the Room component so that it can call that method and modify the parent component
        This takes care of the case where we leave a room and the home page is aware of that as well
        notice that we didn't add parentheses to the method meaning we are passing it not calling it
            <Route 
                path="/room/:roomCode" 
                render={(props) => {
                    return <Room {...props} leaveRoomCallback={this.clearRoomCode}
                }}
            />
    */
    render(){
        return (
            <Router>
                <Switch>
                    <Route exact path="/" render={() => {
                        return this.state.roomCode ? (
                            <Redirect to={`/room/${this.state.roomCode}`}/>
                            ) : 
                            this.renderHomePage();
                        }}
                    />    
                    <Route path="/join" component={RoomJoinPage}/>
                    <Route path="/info" component={Info}/>
                    <Route path="/create" component={CreateRoomPage}/>
                    <Route 
                        path="/room/:roomCode" 
                        render={(props) => {
                            return <Room {...props} leaveRoomCallback={this.clearRoomCode} />;
                        }}
                    />
                </Switch>
            </Router>
            );
    }
}
