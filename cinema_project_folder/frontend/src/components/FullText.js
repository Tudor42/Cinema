import React from 'react';
import FilmList from './Film/FilmList';
import ClientList from './Clienti/ClientList';
import axios from 'axios';
import {Input, Button, Container, Row, Col, InputGroup} from 'reactstrap';
import { API_URL } from '../constants';
import Pagination from './Pagination';

export default class FullText extends React.Component{
    state = {
        clients: [],
        films: [],
        page_clients: 0,
        max_page_clients: 0,
        page_films: 0,
        max_page_films: 0,
        text: ""
    }

    changePageClients = async (val)=>{
        await this.setState({page_clients: val});
        this.resetState()
    }

    changePageFilms = async (val)=>{
        await this.setState({page_films: val});
        this.resetState()
    }

    searchFilms = () =>{
        axios.put(API_URL + "full_text_films/", {"text": this.state.text, "page": this.state.page_films}).then(
            res => {
                this.setState({ 
                    films: res.data['data'],
                    max_page_films: res.data['maxpage'],
                    page_films: res.data['page']
                })
            }
        ).catch(
            ()=>{}
        )
    }

    searchClients = () =>{
        axios.put(API_URL + "full_text_cards/", {"text": this.state.text, "page": this.state.page_clients}).then(
            res => {
                this.setState({ 
                    clients: res.data['data'],
                    max_page_clients: res.data['maxpage'],
                    page_clients: res.data['page']
                })
            }
        ).catch(
            ()=>{}
        )
    }

    resetState = () => {
        this.searchFilms();
        this.searchClients();
    }

    render(){
        return (
            <Container style={{ marginTop: "20px", marginLeft: "180px" }}>
                <Row>
                    <InputGroup>
                        <Input name="text" type="text" onChange={e=>this.setState({text: e.target.value})}/>
                        <Button onClick={this.resetState}>Search</Button>
                    </InputGroup>
                </Row>
                <br/>
                <Row>
                    <Col>
                        <Pagination
                            page={this.state.page_films}
                            maxPage={this.state.max_page_films}
                            changePage={this.changePageFilms}
                        />
                        <FilmList
                            films={this.state.films}
                            resetState={this.resetState}
                        />
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <Pagination
                            page={this.state.page_clients}
                            maxPage={this.state.max_page_clients}
                            changePage={this.changePageClients}
                        />
                        <ClientList
                            clients={this.state.clients}
                            resetState={this.resetState}
                        />
                    </Col>
                </Row>
            </Container>
        )
    }
}