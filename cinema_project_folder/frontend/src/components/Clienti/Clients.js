import React, { Component } from "react";
import { Col, Container, Row, Button, Label, InputGroup, Input } from "reactstrap";
import ClientList from "./ClientList";
import NewModal from "../NewModal";
import axios from "axios";
import InputDate from "../InputDate";
import "../../UndoRedo";
import { API_URL } from "../../constants";
import Pagination from "../Pagination";

class Clients extends Component {
    state = {
        clients: [],
        date_gte: "",
        date_lte: "",
        n: "",
        max_page: 0,
        page: 0,
    };

    sort = false;
    color = '#ff0000';

    getCardsMaxPages = async () => {
        await axios.get(API_URL + 'cards/maxpages/').then(res => this.setState({ max_page: res.data}));
        if (this.state.max_page == 0)
            this.setState({ max_page: 1})
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
        return date;
    }

    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };

    change_sort(){
        this.sort = !this.sort;
        this.resetState();
    }

    onChange= e=>{
        if(e.target.name === "date_lte"){
            e.target.value = this.convert_date(e.target.value, false);
            e.target.min = this.convert_date(e.target.min, false);
            if(e.target.value>=e.target.min){
                this.setState({[e.target.name]: e.target.value});
            }else{
                this.setState({[e.target.name]: this.state.date_gte});
            }
            return;
        }
        if(e.target.name === "date_gte"){
            e.target.value = this.convert_date(e.target.value, false);
            if(this.state.date_lte!=="" && this.state.date_lte < e.target.value){
                this.setState({[e.target.name]: e.target.value, ['date_lte']: e.target.value});
                return;
            }
            this.setState({[e.target.name]: e.target.value});
            return;
        }
        if(e.target.name === "n"){
            if(e.target.value.match(/^[0-9]+$/) == null && e.target.value != ""){
                this.setState({[e.target.name]: this.state.n});
                return;
            }else{
                this.setState({[e.target.name]: e.target.value});
                return;
            }
        }
    }

    componentDidMount() {
        this.resetState();
    }



    addPointsClient = () =>{
        global.waitModal.turn_on();
        axios.put(API_URL+'cards/add_points/', {
            'date_gte': this.state.date_gte,
            'date_lte': this.state.date_lte,
            'n': this.state.n
        }).then(res =>{ 
            global.undo_redo.add_undo_clear_redo(4, 'cards', res.data['prevdata'], res.data['postdata']);
            global.waitModal.turn_off();
            this.resetState()
        })
        .catch(()=> {global.waitModal.turn_off();});
    }

    getClientsAscend = () =>{
        axios.get(API_URL+'cards/ascending/'+this.state.page).then(
            res => this.setState(
                    { 
                        clients: res.data['data'],
                        max_page: res.data['maxpage'],
                        page: res.data['page']
                    }
                )
        );
    }

    getClients = () => {
        axios.get(API_URL+'cards/page/' + this.state.page).then(
            res => this.setState(
                    { 
                        clients: res.data['data'],
                        max_page: res.data['maxpage'],
                        page: res.data['page']
                    }
                )
        );
    };

    resetState = async () => {
        if(this.sort){
            this.color = '#4CAF50';
            this.getClientsAscend();
        }
        else{
            this.color = '#ff0000';
            this.getClients();
        }
    };

    changePage = async (val)=>{
        await this.setState({page: val});
        this.resetState()
    }

    render() {
        return (
            <Container style={{ marginTop: "20px", marginLeft: "180px" }}>
                <Pagination
                    page={this.state.page}
                    maxPage={this.state.max_page}
                    changePage={this.changePage}
                />
                <Row>
                    <Col>
                        <ClientList
                            clients={this.state.clients}
                            resetState={this.resetState}
                        />
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <NewModal create={true} resetState={this.resetState} title='client'/>
                        <Button onClick={()=>this.change_sort()} 
                        style={{
                            'position': 'relative',
                            'left': '20px',
                            'background-color': this.color
                        }}>
                            SortByNumberOfPoints
                        </Button>
                    </Col>
                </Row>
                <hr
                    style={{
                        color: 'white',
                        height: '2px'
                    }}
                />
                <Row>
                    <Col
                        style={{
                            color: 'white',
                        }}>
                        <Label>Add points to clients that have the birthday in a given interval:</Label>
                        <br/>
                        <div
                            style={{width: '50%'}}>
                        <InputDate
                            noEditableText={true}
                            name="date_gte"
                            onChange={this.onChange}
                            bad_req={{is_bad: false, data: null}}
                            defaultIfEmpty={this.defaultIfEmpty}
                            data={this.convert_date(this.state.date_gte, true)}
                            title="Start date"
                            id="di7"
                        />
                        <br/>
                        <InputDate
                            noEditableText={true}
                            name="date_lte"
                            onChange={this.onChange}
                            bad_req={{is_bad: false, data: null}}
                            defaultIfEmpty={this.defaultIfEmpty}
                            data={this.convert_date(this.state.date_lte, true)}
                            title="Finish date"
                            id="di8"
                            min={this.state.date_gte}
                        />
                        <br/>
                            <Label>Number of points:</Label>
                        <InputGroup>
                            <Input name="n" type="text" onChange={this.onChange}
                            value={this.defaultIfEmpty(this.state.n)}/>
                            <Button onClick={this.addPointsClient} color="success">
                                Add
                            </Button>
                        </InputGroup>
                        </div>
                    </Col>
                </Row>
                <InputGroup
                style={{
                    position: "fixed",
                    bottom: "20px",
                    left: "20px",
                    color: 'green',
                    width: '160px'
                }}>
                    <Button onClick={
                        async ()=>{
                            await global.undo_redo.undo();
                            this.resetState();
                        }}
                    color='warning'>
                        Undo
                    </Button>
                    <Button onClick={
                        async ()=>{
                            await global.undo_redo.redo();
                            this.resetState();
                        }}
                    color='info'>
                        Redo
                    </Button>
                </InputGroup>
            </Container>
        );
    }
}

export default Clients;