import React, { Component } from 'react';
import '../App/App.css';
import Button from '@material-ui/core/Button';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

//import Input from '@material-ui/core/Input';

//import { ThemeProvider } from '@material-ui/styles';
import axios from 'axios'
import {withRouter} from "react-router-dom";
const config = {
  headers: {'Access-Control-Allow-Origin': '*'}
};

const Print = (props) => (
    <h2>
        {props.message} 
        {/* access message property of props */}
    </h2>
)

const BootstrapButton = withStyles({
    root: {
      boxShadow: 'none',
      textTransform: 'none',
      fontSize: 16,
      padding: '6px 12px',
      border: '1px solid',
      lineHeight: 1.5,
      backgroundColor: '#007bff',
      color: '#ffedee',
      borderColor: '#007bff',
      fontFamily: [
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        '"Helvetica Neue"',
        'Arial',
        'sans-serif',
        '"Apple Color Emoji"',
        '"Segoe UI Emoji"',
        '"Segoe UI Symbol"',
      ].join(','),
      '&:hover': {
        backgroundColor: '#0069d9',
        borderColor: '#0062cc',
      },
      '&:active': {
        boxShadow: 'none',
        backgroundColor: '#0062cc',
        borderColor: '#005cbf',
      },
      '&:focus': {
        boxShadow: '0 0 0 0.2rem rgba(0,123,255,.5)',
      },
    },
  })(Button);

class SearchBar extends Component {
  constructor (props) {
    super(props)
    this.state = {
      location: '',
      topic: ''
    }
  }

  handleSearchLoc (e) {
    this.setState({ location: e.target.value})
  }

  handleSearchTop (e) {
    this.setState({ topic: e.target.value})
  }

  handleGoClick =()=> {
    axios.post('http://127.0.0.1:5000/search', {
        location: this.state.location,
        topic: this.state.topic
      },config)
      .then( (response) =>{
        console.log(response);
        const payload = response.data; 
        this.props.history.push({
          pathname:"/result",
          state:payload
        })
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  render () {
    return (
        <div className='searchbar-container'>
            <Print message="Give power to the people." />
            {/* <img 
                className="App-logo"
                src="https://images.pexels.com/photos/20787/pexels-photo.jpg?auto=compress&cs=tinysrgb&h=350"
                alt="new"
            /> */}
            <form method="POST" className='Search-Bar' onSubmit={e => e.preventDefault()}>
            <TextField
                id="location"
                label="Enter Location"
                //className={classes.textField}
                value={this.state.location}
                onChange={this.handleSearchLoc.bind(this)}
                margin="normal"
                variant="filled"
                style = {{width: 650,
                    backgroundColor: "white"}}
                //backgroundColor = theme.palette.common.white
            />
            <br />
            <TextField
                id="text"
                label="Enter Topic"
                value={this.state.topic}
                onChange={this.handleSearchTop.bind(this)}
                margin="normal"
                variant="filled"
                style = {{width: 650,
                    backgroundColor: "white"
                }}
            />

            <br />
            <BootstrapButton
                type='submit'
                size='large'
                onClick={this.handleGoClick}>
                Search
            </BootstrapButton>
            </form>
            {/* <Print message={"Searching location: " + this.state.location}/> */}
            {/* <Print message={"Searching topic: " + this.state.topic}/> */}
        </div>
    )
  }
}

export default withRouter(SearchBar)