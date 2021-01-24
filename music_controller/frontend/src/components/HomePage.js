import React, { Component } from 'react';
// We don't need to import render because in App.js we are rendering the App component 
// Render the homepage component from the App component

export default class HomePage extends Component{
    constructor(props){
        // Call the constructor of component which is necessary
        super(props);
    }
    render(){
        return <p>This is the home page</p>
    }
}
