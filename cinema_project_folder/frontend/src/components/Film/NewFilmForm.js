import React from "react";
import { Button, Form, FormGroup, Input, Label, FormFeedback } from "reactstrap";
import axios from "axios";
import "../../UndoRedo";
import { API_URL } from "../../constants";
class NewFilmForm extends React.Component {
    state = {
        id: null,
        titlu: null,
        an_aparitie: null,
        pret: null,
        in_program: false
    };

    bad_req = {
        data: null,
        is_bad: false
    }

    componentDidMount() {
        if (this.props.film) {
            const { id, titlu, an_aparitie, pret, in_program } = this.props.film;
            this.setState({ id, titlu, an_aparitie, pret, in_program });
        }
    }

    onChange = e => {
        if(e.target.name === "in_program"){
            this.setState({["in_program"]: !this.state.in_program});
        }else
            this.setState({ [e.target.name]: e.target.value });
    };

    createFilm = e => {
        global.waitModal.turn_on();
        e.preventDefault();
        axios.post(API_URL+'films/', this.state).then(res => {
            global.undo_redo.add_undo_clear_redo(1, 'films', null, res.data);
            this.props.resetState();
            this.props.toggle();
            global.waitModal.turn_off();
        })
        .catch((error) => {
            this.bad_req.is_bad = true;
            this.bad_req.data = error.response.data;
            this.setState(this.state);
            global.waitModal.turn_off();
            }
        );
    };

    editFilm = e => {
        e.preventDefault();
        global.waitModal.turn_on();
        axios.put(API_URL+ 'films/' + this.state.id, this.state).then(res => {
            global.undo_redo.add_undo_clear_redo(3, 'films', res.data['prevdata'], res.data['postdata']);
            this.props.resetState();
            this.props.toggle();
            global.waitModal.turn_off();
        })
        .catch((error) => {
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
            <Form >
                <FormGroup>
                    <Label for="titlu">Title:</Label>
                    <Input
                        type="text"
                        name="titlu"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.titlu)}
                        invalid={this.bad_req.is_bad && this.bad_req.data['titlu']}
                    />
                    {this.bad_req.is_bad?(
                    <FormFeedback>
                            {this.bad_req.data['titlu']}
                    </FormFeedback>):(<div/>)}
                </FormGroup>
                <FormGroup>
                    <Label for="an_aparitie">Release year:</Label>
                    <Input
                        type="number"
                        name="an_aparitie"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.an_aparitie)}
                        invalid={this.bad_req.is_bad && this.bad_req.data['an_aparitie']}
                    />
                    {this.bad_req.is_bad?(
                    <FormFeedback>
                            {this.bad_req.data['an_aparitie']}
                    </FormFeedback>):(<div/>)}
                </FormGroup>
                <FormGroup>
                    <Label for="pret">Price:</Label>
                    <Input
                        type="number"
                        name="pret"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.pret)}
                        invalid={this.bad_req.is_bad && this.bad_req.data['pret']}
                    />
                    {this.bad_req.is_bad?(
                    <FormFeedback>
                            {this.bad_req.data['pret']}
                    </FormFeedback>):(<div/>)}
                </FormGroup>
                <FormGroup>
                    <Label for="in_program">In program: </Label>
                    <Input
                        type="checkbox"
                        name="in_program"
                        onChange={this.onChange}
                        checked={this.defaultIfEmpty(this.state.in_program)}
                        invalid={this.bad_req.is_bad && this.bad_req.data['in_program']}
                    />
                    {this.bad_req.is_bad?(
                    <FormFeedback>
                            {this.bad_req.data['in_program']}
                    </FormFeedback>):(<div/>)}
                </FormGroup>
                <Button onClick={this.props.film ? this.editFilm : this.createFilm}>Send</Button>
            </Form>
        );
    }
}

export default NewFilmForm;