import React from 'react';
import { FormGroup, Input, Label, FormFeedback, InputGroup, InputGroupText } from "reactstrap";
import '../css/datepick.css'

export default class InputDate extends React.Component{
    /*
        Parameters to pass into the class
        name - name of the variable to change
        onChange function
        bad_req - variable from parent class to give feedback
            on bad inputs
        defaultIfEmpty function
        data variable
        id - variable
        noEditableText - True/false or empty
    */
    render(){
        let funct = this.props.noEditableText? null : this.props.onChange;
        return(
            <FormGroup>
            <Label for={this.props.name}>{this.props.title}: </Label>
            <InputGroup>
                <Input
                    type="text"
                    name={this.props.name}
                    onChange={funct}
                    value={this.props.defaultIfEmpty(this.props.data)}
                    invalid={this.props.bad_req.is_bad && this.props.bad_req.data[this.props.name]}
                />
                <input
                    type="date"
                    name={this.props.name}
                    onChange={this.props.onChange}
                    invalid={this.props.bad_req.is_bad && this.props.bad_req.data[this.props.name]}
                    id={this.props.id}
                    style={{
                        'zIndex': '0',
                        'width': '0',
                        'height': '0',
                        'border-block-color': 'white',
                    }}
                    min={this.props.min}
                />
            <Label for={this.props.id}
                    style={{
                        'height': '10px',
                    }}>
            <InputGroupText>
                    Pick
            </InputGroupText>
            </Label>
            {this.props.bad_req.is_bad?(
            <FormFeedback>
                    {this.props.bad_req.data[this.props.name]}
            </FormFeedback>):(<div/>)}
            </InputGroup>
        </FormGroup>
        );
    }
    
}