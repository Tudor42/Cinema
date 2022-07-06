import React, { Component } from "react";
import { Table } from "reactstrap";
import NewModal from "../NewModal";
import ConfirmRemovalModal from "../ConfirmRemovalModal";

class FilmList extends Component {
    
    render() {
        const films = this.props.films;
        return (
            <Table dark>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Year</th>
                        <th>Price</th>
                        <th>In program</th>
                        <th>Nr of bookings</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {!films || films.length <= 0 ? (
                        <tr>
                            <td colSpan="6" align="center">
                                <b>Ops, no one here yet</b>
                            </td>
                        </tr>
                    ) : (
                        films.map(film => (
                            <tr key={film.id}>
                                <td>{film.id}</td>
                                <td>{film.titlu}</td>
                                <td>{film.an_aparitie}</td>
                                <td>{film.pret}</td>
                                <td>{film.in_program.toString()}</td>
                                <td>{film.num_of_bookings}</td>
                                <td align="center">
                                    <NewModal
                                        create={false}
                                        film={film}
                                        resetState={this.props.resetState}
                                        title="film"
                                    />
                                    &nbsp;&nbsp;
                                    <ConfirmRemovalModal
                                        id={film.id}
                                        resetState={this.props.resetState}
                                        table="films"
                                    />
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </Table>
        );
    }
}

export default FilmList;