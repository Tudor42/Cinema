import React from "react";
import { InputGroup, Button, Input, Badge } from "reactstrap";

export default class Pagination extends React.Component{
    state = {
        input_page: "",
    }

    render(){
        return(
            <div>
                <InputGroup>
                    <InputGroup
                        style={{
                            width: '14%'
                        }}
                    >
                        <Button
                            onClick={() => this.props.changePage(0)}
                        >
                            {'<<'}
                        </Button>
                        <Button
                            onClick={() => {if (this.props.page > 0) this.props.changePage(this.props.page - 1)}}
                        >
                            {'<'}
                        </Button>
                        <Button
                            onClick={() => {if (this.props.page<this.props.maxPage-1) this.props.changePage(this.props.page + 1)}}
                        >
                            {'>'}
                        </Button>
                        <Button
                            onClick={() => this.props.changePage(this.props.maxPage - 1)}
                        >
                            {'>>'}
                        </Button>
                    </InputGroup>
                    &nbsp;
                    <InputGroup
                        style={{
                            width: "25%"
                        }}
                    >
                        <Input
                            type='number'
                            onChange={e => {this.setState({input_page: e.target.value})}}
                        >
                            
                        </Input>
                        <Button
                            onClick={
                                () =>{
                                    if((parseInt(this.state.input_page) - 1)>=0 && parseInt(this.state.input_page)<=this.props.maxPage){
                                        this.props.changePage(this.state.input_page - 1)
                                    }
                                }
                            }
                        >
                            GoTo
                        </Button>
                    </InputGroup>
                    <Badge color="primary">
                        {this.props.page + 1}/{this.props.maxPage}
                    </Badge>
                </InputGroup>
            </div>
        )
    }

}