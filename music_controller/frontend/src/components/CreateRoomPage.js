import React, { Component } from 'react';
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import { Collapse } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";

export default class CreateRoomPage extends Component{
    // If we don't pass any of these props anywhere, by default they will have those values
    // With this we can change this.state inside our constructor so everything has this.props...
    static defaultProps = {
        votesToSkip: 2, 
        guestCanPause: true,
        update: false,
        roomCode: null, 
        updateCallBack: () => { },
    };

    constructor(props){
        // Call the constructor of component which is necessary
        super(props);
        // To keep track what's in our form (such as buttons and text value) below we use states to send it to the back-end
        // If these states are updated it forces the components to update
        // So every time the radio button or text is updated we will update the state and show whatever the state is
        // When you press the Create Room button we'll look at the current state and send that info to the back-end
        // they will take the value of whatever is passed through in props
        // This way we are not using hardcoded values
        this.state = {
            guestCanPause: this.props.guestCanPause,
            votesToSkip: this.props.votesToSkip,
            errorMsg: "",
            successMsg: "",
        };

        // We are binding the method handleRoomButtonPressed to the class as well as the other methods
        // This will enable us to use the keyword this
        this.handleRoomButtonPressed = this.handleRoomButtonPressed.bind(this);
        this.handleVotesChange = this.handleVotesChange.bind(this);
        this.handleGuessCanPauseChange = this.handleGuessCanPauseChange.bind(this);
        this.handleUpdateButtonPressed = this.handleUpdateButtonPressed.bind(this);
    }

    // e is the object that called this function
    handleVotesChange(e) {
        // this.setState is used to update the states
        // e.target.value corresponds to the text field we have and it'll take the value
        this.setState({
            votesToSkip: e.target.value,
        });
    }

    // it is used as an onChange inside the tag TextField for example
    handleGuessCanPauseChange(e) { 
        this.setState({
            guestCanPause: e.target.value === 'true' ?  true: false,
        });
    }

    handleRoomButtonPressed() {
        // console.log(this.state) this will print out to the console {guestCanPause: true, votesToSkip: "4"}
        // the fields inside the body need to match those in the server
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                votes_to_skip: this.state.votesToSkip,
                guest_can_pause: this.state.guestCanPause,
            }),
        };
        // send a request to '/api/create-room' with the requestOptions payload
        // 'then' means once we get a response we take it and convert it to json and then we do 
        // something with the data which is basically the response.json() object
        // this line: .then((data) => this.props.history.push('/room/' + data.code));
        // redirects the user when they click the button Create a Room to that url
        fetch('/api/create-room', requestOptions)
            .then((response) => response.json())
            .then((data) => this.props.history.push('/room/' + data.code));
    }

    // Update Room button
    // PATCH will trigger the method patch() inside UpdateRoom class
    handleUpdateButtonPressed(){
        const requestOptions = {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                votes_to_skip: this.state.votesToSkip,
                guest_can_pause: this.state.guestCanPause,
                code: this.props.roomCode,
            }),
        };
        fetch('/api/update-room', requestOptions)
        .then((response) => {
            if (response.ok){
                this.setState({
                    successMsg: "Room updated successfully!",
                });
            } else {
                this.setState({
                    errorMsg: "Error updating room...",
                });
            }
            this.props.updateCallback();
        });
       
        
    }

    // We are going to have 2 methods one that creates the buttons to Create a New Room
    // and another method that creates the buttons to Update a Room
    renderCreateButtons(){
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Button color="primary" variant="contained" onClick={this.handleRoomButtonPressed}>
                        Create A Room
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color="secondary" variant="contained" to="/" component={Link}>
                        Back
                    </Button>
                </Grid>
            </Grid>
        );
    }

    renderUpdateButtons(){
        return (
            <Grid item xs={12} align="center">
                <Button 
                    color="primary" 
                    variant="contained" 
                    onClick={this.handleUpdateButtonPressed}>
                    Update Room
                </Button>
            </Grid>
        );
    }

    render(){
        const title = this.props.update ? "Update Room" : "Create a Room";

        // Grid helps us aligning elements either horizontally or vertically
        // The container keyword is saying that we'll align everything in a column-like structure
        // The spacing keyword means that 1 is 8px and so on
        return(
        <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Collapse in={this.state.errorMsg != "" || this.state.successMsg != ""}>
                    {this.state.successMsg != "" ? (
                        <Alert severity="success" onClose={() => {this.setState({successMsg: ""});}}>{this.state.successMsg}</Alert>
                    ) : (
                        <Alert severity="error" onClose={() => {this.setState({errorMsg: ""});}}>{this.state.errorMsg}</Alert>
                    )}
                </Collapse>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography component='h4' variant='h4'>
                    {title}
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl component="fieldset">
                    <FormHelperText>
                        <div align='center'>
                            Guest Control of Playback State
                        </div>
                    </FormHelperText>
                    <RadioGroup 
                        row 
                        defaultValue={this.props.guestCanPause.toString()} 
                        onChange={this.handleGuessCanPauseChange}
                    >
                        <FormControlLabel 
                            value="true" 
                            control={ <Radio color="primary"/>}
                            label="Play/Pause"
                            labelPlacement="bottom"
                        />
                        <FormControlLabel 
                            value="false" 
                            control={ <Radio color="secondary"/>}
                            label="No Control"
                            labelPlacement="bottom"
                        />
                    </RadioGroup>
                </FormControl>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl>
                    <TextField 
                        required={true} 
                        type="number" 
                        onChange={this.handleVotesChange}
                        defaultValue={this.state.votesToSkip} 
                        inputProps={{
                            min:1,
                            style: {textAlign: "center"},
                        }}
                    />
                    <FormHelperText>
                        <div align="center">
                            Votes Required to Skip Song
                        </div>
                    </FormHelperText>
                </FormControl>
            </Grid>
            {this.props.update 
            ? this.renderUpdateButtons()
            : this.renderCreateButtons()}
        </Grid>
        );
    }
}
