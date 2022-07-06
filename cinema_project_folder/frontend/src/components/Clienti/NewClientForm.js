import React from "react";
import { Button, Form, FormGroup, Input, Label, FormFeedback} from "reactstrap";
import InputDate from "../InputDate";

import axios from "axios";

import "../../UndoRedo"

import { API_URL } from "../../constants";

class NewClientForm extends React.Component {
    state = {
        id: null,
        nume: null,
        prenume: null,
        CNP: null,
        data_nasterii: null,
        data_inregistrarii: null,
        puncte: null,
    };

    bad_req = {
            data: null,
            is_bad: false
    };

    componentDidMount() {
        if (this.props.client) {
            const { id, nume, prenume, CNP, data_nasterii, data_inregistrarii, puncte } = this.props.client;
            this.setState({ id, nume, prenume, CNP, data_nasterii, data_inregistrarii, puncte });
        }
    }

    onChange = e => {
        if((e.target.name === "data_nasterii" || e.target.name === "data_inregistrarii") && e.target.value){
            this.setState({ [e.target.name]: this.convert_date(e.target.value, true)});
            return
                
        }
        this.setState({ [e.target.name]: e.target.value });
    };

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

    createClient = e => {
        let d1 = this.state.data_nasterii;
        this.state.data_nasterii = this.convert_date(this.state.data_nasterii, false)

        let d2 = this.state.data_inregistrarii;
        this.state.data_inregistrarii = this.convert_date(this.state.data_inregistrarii, false)

        e.preventDefault();
        global.waitModal.turn_on();
        axios.post(API_URL+'cards/', this.state).then(res => {
            global.undo_redo.add_undo_clear_redo(1, "cards", null, res.data);
            this.props.resetState();
            this.props.toggle();
            global.waitModal.turn_off();
        })
        .catch((error) => {
                    this.state.data_nasterii = d1;
                    this.state.data_inregistrarii = d2;
                    this.bad_req.is_bad = true;
                    this.bad_req.data = error.response.data;
                    this.setState(this.state);
                    global.waitModal.turn_off();
                }
        );
    };

    editClient = e => {
        let d1 = this.state.data_nasterii;
        this.state.data_nasterii = this.convert_date(this.state.data_nasterii, false);

        let d2 = this.state.data_inregistrarii;
        this.state.data_inregistrarii = this.convert_date(this.state.data_inregistrarii, false);        

        e.preventDefault();
        global.waitModal.turn_on();
        axios.put(API_URL +'cards/'+ this.state.id, this.state).then(res => {
            global.undo_redo.add_undo_clear_redo(3, "cards", res.data['prevdata'], res.data['postdata']);
            this.props.resetState();
            this.props.toggle();
            global.waitModal.turn_off();
        })  
        .catch((error) => {
            this.state.data_nasterii = d1;
            this.state.data_inregistrarii = d2;
            this.bad_req.is_bad = true;
            this.bad_req.data = error.response.data;
            this.setState(this.state);
            global.waitModal.turn_off();
        }
        );
    };

    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };

    render() {
        return (
            <Form>
                <FormGroup>
                    <Label for="nume">Last name:</Label>
                    <Input
                        type="text"
                        name="nume"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.nume)}
                        invalid={this.bad_req.is_bad && this.bad_req.data['nume']}
                    />
                    {this.bad_req.is_bad?(
                    <FormFeedback>
                            {this.bad_req.data['nume']}
                    </FormFeedback>):(<div/>)}
                </FormGroup>
                <FormGroup>
                    <Label for="prenume">First name:</Label>
                    <Input
                        type="text"
                        name="prenume"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.prenume)}
                        invalid={this.bad_req.is_bad && this.bad_req.data['prenume']}
                    />
                    {this.bad_req.is_bad?(
                    <FormFeedback>
                            {this.bad_req.data['prenume']}
                    </FormFeedback>):(<div/>)}
                </FormGroup>
                <FormGroup>
                    <Label for="CNP">CNP:</Label>
                    <Input
                        type="text"
                        name="CNP"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.CNP)}
                        invalid={this.bad_req.is_bad && this.bad_req.data['CNP']}
                    />
                    {this.bad_req.is_bad?(
                    <FormFeedback>
                            {this.bad_req.data['CNP']}
                    </FormFeedback>):(<div/>)}
                </FormGroup>
                <InputDate 
                    name="data_nasterii"
                    onChange={this.onChange}
                    bad_req={this.bad_req}
                    defaultIfEmpty={this.defaultIfEmpty}
                    data={this.state.data_nasterii}
                    title="Birth date"
                    id="d1"
                />
                <InputDate
                    name="data_inregistrarii"
                    onChange={this.onChange}
                    bad_req={this.bad_req}
                    defaultIfEmpty={this.defaultIfEmpty}
                    data={this.state.data_inregistrarii}
                    title="Regitration date"
                    id="d2"
                />
                <FormGroup>
                    <Label for="puncte">Points </Label>
                    <Input
                        type="number"
                        name="puncte"
                        onChange={this.onChange}
                        invalid={this.bad_req.is_bad && this.bad_req.data['puncte']}
                        value={this.defaultIfEmpty(this.state.puncte)}
                    />
                    {this.bad_req.is_bad?(
                    <FormFeedback>
                            {this.bad_req.data['puncte']}
                    </FormFeedback>):(<div/>)}
                </FormGroup>
                <Button onClick={this.props.client ? this.editClient : this.createClient}>Send</Button>
            </Form>
        );
    }
}

export default NewClientForm;