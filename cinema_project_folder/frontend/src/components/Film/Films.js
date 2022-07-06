import React, { Component } from "react";
import { Button, Col, Container, Row, InputGroup } from "reactstrap";
import FilmList from "./FilmList";
import NewModal from "../NewModal";
import axios from "axios";
import GenerateRandom from "./functionalities/GenerateRandom";
import { API_URL } from "../../constants";
import Pagination from "../Pagination";


class Films extends Component {
    state = {
        films: [],
        max_page: 0,
        page: 0,
    };
    
    sort = false;

    change_sort(){
        this.sort = !this.sort;
        this.resetState();
    }

    componentDidMount() {
        this.resetState();
    }

    getFilmsDescend = () => {
        axios.get(API_URL+'films/descending/' + this.state.page).then(
                res => this.setState(
                        { 
                            films: res.data['data'],
                            max_page: res.data['maxpage'],
                            page: res.data['page']
                        }
                    )
            );
    };

    getFilms = () => {
        axios.get(API_URL+'films/page/' + this.state.page).then(
            res => this.setState(
                    { 
                        films: res.data['data'],
                        max_page: res.data['maxpage'],
                        page: res.data['page']
                    }
                )
        );
    };

    resetState = async () => {
        if(this.sort){
            this.color = '#4CAF50';
            this.getFilmsDescend();
        }
        else{
            this.color = '#ff0000';
            this.getFilms();
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
                        <FilmList
                            films={this.state.films}
                            resetState={this.resetState}
                        />
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <NewModal create={true} resetState={this.resetState} title="film"/>
                        <Button onClick={()=>this.change_sort()} 
                        style={{
                            'position': 'relative',
                            'left': '20px',
                            'background-color': this.color
                        }}>
                            SortByNumberOfBookings
                        </Button>
                    </Col>
                    <Col>
                        <GenerateRandom resetState={this.resetState}/>
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

export default Films;