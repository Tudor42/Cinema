import React, { Component } from "react";
import { Col, Container, Input, InputGroup, Row, Label, Button } from "reactstrap";
import BookingList from "./BookingList";
import NewModal from "../NewModal";
import axios from "axios";
import InputDate from "../InputDate";

import "../../UndoRedo"
import { API_URL } from "../../constants";
import Pagination from "../Pagination";

class Bookings extends Component {
    state = {
        bookings: [],
        time_gte: "",
        time_lte: "",
        time_filter: false,
        date_gte: "",
        date_lte: "",
        max_page: 0,
        page: 0,
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

    color = '#ff0000';

    changeTimeFilter(){
        this.state.time_filter = !this.state.time_filter;
        this.resetState();
    }

    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };

    onChange= e=>{
        if(e.target.name === "time_lte"){
            if(e.target.value>e.target.min){
                this.setState({[e.target.name]: e.target.value});
            }else{
                this.setState({[e.target.name]: this.state.time_gte});
            }
            return;
        }
        if(e.target.name === "time_gte"){
            if(this.state.time_lte!=="" && this.state.time_lte < e.target.value){
                this.setState({[e.target.name]: e.target.value, ['time_lte']: e.target.value});
                return;
            }
        }

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
        }

        this.setState({[e.target.name]: e.target.value});
    }

    componentDidMount() {
        this.resetState();
    }

    deleteBookings = () => {
        global.waitModal.turn_on();
        axios.put(API_URL+'bookings_filter/1', {date_gte: this.convert_date(this.state.date_gte, false), 
            date_lte: this.convert_date(this.state.date_lte, false)}).then(res => {
                global.undo_redo.add_undo_clear_redo(6, 'bookings', res.data, null);
                this.resetState();
                global.waitModal.turn_off();
            })
            .catch(() =>{global.waitModal.turn_off();});
    }

    getBookingsTimeInterval = () => {
        axios.put(API_URL+'bookings_filter/2', {time_gte: this.state.time_gte, 
            time_lte: this.state.time_lte, page: this.state.page}).then(
                res => this.setState(
                    { 
                        bookings: res.data['data'],
                        max_page: res.data['maxpage'],
                        page: res.data['page']
                    }
                )
            )
            .catch(() =>{
                this.state.time_filter = !this.state.time_filter;
                this.resetState();
            });
    }

    getBookings = () => {
        axios.get(API_URL+'bookings/page/' + this.state.page).then(
            res => this.setState(
                { 
                    bookings: res.data['data'],
                    max_page: res.data['maxpage'],
                    page: res.data['page']
                }
            )
        );
    };

    resetState = () => {
        if(this.state.time_filter){
            this.color = '#4CAF50';
            this.getBookingsTimeInterval();
        }
        else{
            this.color = '#ff0000';
            this.getBookings();
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
                        <BookingList
                            bookings={this.state.bookings}
                            resetState={this.resetState}
                        />
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <NewModal create={true} resetState={this.resetState} title='booking'/>
                    </Col>
                </Row>
                <br/>
                <Row>
                    <Col
                        style={{
                            color: 'white',
                        }}>
                        <Label>Delete bookings:</Label>
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
                            id="di5"
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
                            id="di6"
                            min={this.state.date_gte}
                        />
                        <br/>
                        <Button onClick={this.deleteBookings} color="danger">
                            Delete
                        </Button>
                        </div>
                    </Col>
                </Row>
                <hr
                    style={{
                        color: 'white',
                        height: '2px'
                    }}
                />

                <Row>
                    <Col>
                        
                        <Label
                        style={{
                            color: "white"
                        }}>
                            Bookings between time
                        </Label>
                        <br/>
                        <Label for="time_gte"
                            style={{
                                color: "white"
                            }}
                        >From:</Label>
                        <Label for="time_lte"
                            style={{
                                color: "white",
                                paddingLeft: '200px'
                            }}
                        >Till:</Label>
                        <InputGroup
                            style={{
                                width: '600px'
                            }}
                            >
                            <Input
                                type="time"
                                name="time_gte"
                                onChange={this.onChange}
                                value={this.defaultIfEmpty(this.state.time_gte)}
                                />
                            <Input 
                                type="time"
                                name="time_lte"
                                onChange={this.onChange}
                                value={this.defaultIfEmpty(this.state.time_lte)}
                                min={this.state.time_gte}
                                />
                            <Button onClick={()=>this.changeTimeFilter()} 
                            style={{
                                'position': 'relative',
                                'left': '20px',
                                'background-color': this.color
                            }}>
                                Filter by time
                            </Button>
                        </InputGroup>
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

export default Bookings;