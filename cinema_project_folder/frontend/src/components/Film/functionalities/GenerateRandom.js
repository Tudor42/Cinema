import React from "react";
import axios from "axios";
import { Input, InputGroup, Button } from "reactstrap";
import '../../../UndoRedo.js';
import {API_URL} from "../../../constants.js"


export default class GenerateRandom extends React.Component{
    state ={
        num: null,
    }

    change_num = e=>{
        console.log()
        if(e.target.name === "num"){
            this.setState({num : e.target.value});
        }
    }

    generate_random_movies = () => {
        if(this.state.num && this.state.num > 0){
            global.waitModal.turn_on();
            axios.post(API_URL+'films/generate_random/'+this.state.num).then(
                res=>{
                    global.undo_redo.add_undo_clear_redo(2, 'films', null, res.data);
                    this.props.resetState();
                    global.waitModal.turn_off();
            });
        }
    }

    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };

    render(){
        return(<InputGroup
            style={{
                'left': '20px',
                'width': '300px',
            }}
        >
        <Input
            type="number"
            name="num"
            value={this.defaultIfEmpty(this.state.num)}
            onChange={this.change_num}
        />
        <Button onClick={()=>this.generate_random_movies()} 
        style={{
            'position': 'relative',
            'left': '20px',
            'background-color': '04cfdd'
        }}>
            Generate
        </Button>
        
        </InputGroup>
        )
    }
}