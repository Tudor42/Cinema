import React from "react";
import { Button, Form, FormGroup, Input, Label, FormFeedback, InputGroup } from "reactstrap";
import axios from "axios";
import '../../css/datepick.css';
import InputDate from "../InputDate";

import "../../UndoRedo";

import { API_URL } from "../../constants";
class NewBookingForm extends React.Component {
    state = {
        id: null,
        id_film: null,
        id_card_client: null,
        data: null,
        ora: "00:00",
        str_film: "",
        str_client: "",
    }; // values that are filled in the form
    
    bad_req = {
        data: null, // invalid fields
        is_bad: false // is the field invalid
    }; // to show the fieds that contain invalid data
 
    searched_film = "";
    films = []; // films that are in the program
    // If the booking is made for a movie that is no longer
    // in the program then the booking cant be change unless
    // the movie is changed with a valid one

    searched_card = "";
    cards = []; // all the clients clients

    get_valid_films = () => {
        /*
            Retrieves data from the server with available films
        */
        axios.post(API_URL + "films/property/", {in_program: true, search: this.searched_film}).then(res =>{
                this.films = res.data;
                this.setState(this.state);
           }
        );
    }
    
    get_valid_cards=()=>{
        /*
            Retrieves data from the server with all the clients
        */
        axios.put(API_URL+"full_text_cards/", {"text": this.searched_card, "first_10": true}).then(
            res => {
                this.cards = res.data;
                this.setState(this.state);
            }
        );
    }

    componentDidMount() {
        /*
            Commands to execute whenever the form is opened
        */
        if (this.props.booking) { // puts booking values in the fields if it is an edit
            const { id, id_film, id_card_client, data, ora, str_film, str_client } = this.props.booking;
            this.setState({ id, id_film, id_card_client, data, ora, str_film, str_client });
        }
        this.get_valid_cards();
        this.get_valid_films();
    }

    convert_date(date, conversion){
        /*
            Converts the data between two formats
            1. %dd.%mm.%yyyy 
            and 
            2. %yyyy-%mm-%dd

            conversion value: true
            conversion: second -> first 

            comversion value: false
            conversion: first -> second

            If conversion cant be made the data value is returned
        */
        if(date){
            if(conversion){
                let s = date.split("-");
                if(s.length===3){
                    return s[2]+'.'+s[1]+'.'+s[0];
                }
                return date;
            }
            let s = date.split(".");
            if(s.length===3){
                return s[2]+'-'+s[1]+'-'+s[0];
            }
            return date;
        }
        return null;
    }

    onChange = e => {
        if(e.target.name === "searched_film"){
            this.searched_film = e.target.value;
            this.setState({});
            return;
        }
        
        if(e.target.name === "searched_card"){
            this.searched_card = e.target.value;
            this.setState({});
            return;
        }

        if((e.target.name === "data") && e.target.value){
            this.setState({ [e.target.name]: this.convert_date(e.target.value, true)});
            return;
        }
        this.setState({ [e.target.name]: e.target.value });

    };
    
    createBooking = e => {
        let id = this.state.id_film;
        if(this.state.str_film == "Choose a movie" || this.state.str_film == "No movie in program" || this.state.str_film==null){
            this.state.id_film = null;
        }else{
            this.state.id_film = this.state.str_film.split(' ').pop().slice(1, -1);
        }
        
        let idc = this.state.id_card_client;
        if(this.state.str_client == "No clients yet" || this.state.str_client == "Client" || this.state.str_client==null){
            this.state.id_card_client = null;
        }else{
            this.state.id_card_client = this.state.str_client.split(' ').pop().slice(1, -1);
        }

        let d = this.state.data;
        this.state.data = this.convert_date(this.state.data, false);

        e.preventDefault();
        global.waitModal.turn_on();
        axios.post(API_URL+'bookings/', this.state).then(res => {
            global.undo_redo.add_undo_clear_redo(1, 'bookings', null, res.data);
            this.props.resetState();
            this.props.toggle();
            global.waitModal.turn_off();
        }).catch((error) => {
            this.state.data = d;
            this.state.id_film = id;
            this.state.id_card_client = idc;
            this.bad_req.is_bad = true;
            this.bad_req.data = error.response.data;
            this.bad_req.data["str_film"] = this.bad_req.data["id_film"];
            console.log(this.bad_req.data);
            this.setState(this.state);
            global.waitModal.turn_off();
        });
    };
    
    editBooking = e => {
        let id = this.state.id_film;
        if(this.state.str_film == "Choose a movie" || this.state.str_film == "No movie in program" || this.state.str_film==null){
            this.state.id_film = null;
        }else{
            this.state.id_film = this.state.str_film.split(' ').pop().slice(1, -1);
        }

        let idc = this.state.id_card_client;
        if(this.state.str_client == "No clients yet" || this.state.str_client == "Client" || this.state.str_client==null){
            this.state.id_card_client = null;
        }else{
            this.state.id_card_client = this.state.str_client.split(' ').pop().slice(1, -1);
        }

        let d = this.state.data
        this.state.data = this.convert_date(this.state.data, false);

        e.preventDefault();
        global.waitModal.turn_on();
        axios.put(API_URL+ 'bookings/' + this.state.id, this.state).then(res => {
            global.undo_redo.add_undo_clear_redo(3, 'bookings', res.data['prevdata'], res.data['postdata']);
            this.props.resetState();
            this.props.toggle();
            global.waitModal.turn_off();
        }).catch((error) => {
            this.state.data = d;
            this.state.id_film = id;
            this.state.id_card_client = idc;
            this.bad_req.is_bad = true;
            this.bad_req.data = error.response.data;
            this.bad_req.data["str_film"] = this.bad_req.data["id_film"];
            console.log(this.bad_req.data);
            this.setState(this.state);
            global.waitModal.turn_off();
        });
    };

    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };

    render() {
        return(
            <Form >
                <FormGroup>
                    <Label for="str_film">Film:</Label>
                    <Input
                        type="select"
                        name="str_film"
                        onClick={this.get_valid_films}
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.str_film)}
                        invalid={this.bad_req.is_bad && this.bad_req.data['str_film']}>
                        <option>
                            Choose a movie
                        </option>
                        {!this.films || this.films.length <= 0 ? (
                            <option>
                                No movie in program
                            </option>
                        ) : (
                            this.films.map(
                                film => (
                                    this.searched_film === "" || film.str_reprezentation.toLowerCase().includes(this.searched_film.toLowerCase())?(
                                        <option>
                                            {film.str_reprezentation}
                                        </option>)
                                    :(<div/>)
                                )
                            )
                        )
                        }
                    </Input>
                    {this.bad_req.is_bad?(
                        <FormFeedback>
                            {this.bad_req.data['id_film']}
                        </FormFeedback>):(<div/>)}
                    <br/>
                    <InputGroup>
                        <Input
                            type="text"
                            name="searched_film"
                            onChange={this.onChange}
                            value={this.defaultIfEmpty(this.searched_film)}
                            placeholder="Search films..."
                        />
                    </InputGroup>
                </FormGroup>
                <FormGroup>
                    <Label for="str_client">Client:</Label>
                    <Input
                        type="select"
                        name="str_client"
                        onChange={this.onChange}
                        onClick={this.get_valid_cards}
                        value={this.defaultIfEmpty(this.state.str_client)}
                        invalid={this.bad_req.is_bad && this.bad_req.data['str_client']}
                    >
                        <option>
                            Client
                        </option>
                        {!this.cards || this.cards.length <= 0 ? (
                            <option>
                                No clients yet
                            </option>
                        ) : (
                            this.cards.map(
                                card => (
                                    this.searched_card === "" || card.str_reprezentation.toLowerCase().includes(this.searched_card.toLowerCase())?(
                                        <option>
                                            {card.str_reprezentation}
                                        </option>)
                                    : (<div/>)
                                )
                            )
                        )
                        }
                    </Input>
                    {this.bad_req.is_bad?(
                    <FormFeedback>
                            {this.bad_req.data['id_card_client']}
                    </FormFeedback>):(<div/>)}
                    <br/>
                    <InputGroup>
                        <Input
                            type="text"
                            name="searched_card"
                            onChange={this.onChange}
                            value={this.defaultIfEmpty(this.searched_card)}
                            placeholder="Search clients..."
                        />
                    </InputGroup>
                </FormGroup>
                <InputDate 
                    name="data" 
                    onChange={this.onChange} 
                    bad_req={this.bad_req} 
                    defaultIfEmpty={this.defaultIfEmpty}
                    data={this.state.data}
                    id="d3"
                    title="Data"/>
                <FormGroup>
                    <Label for="ora">Hour: </Label>
                    <Input
                        type="time"
                        name="ora"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.ora)}
                        invalid={this.bad_req.is_bad && this.bad_req.data['ora']}
                    />
                    {this.bad_req.is_bad?(
                    <FormFeedback>
                            {this.bad_req.data['ora']}
                    </FormFeedback>):(<div/>)}
                </FormGroup>
                <Button onClick={this.props.booking ? this.editBooking : this.createBooking}>Send</Button>
            </Form>
        );
    }
}

export default NewBookingForm;