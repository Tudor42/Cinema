import React, { Component } from "react";
import { Table } from "reactstrap";
import NewModal from "../NewModal";
import ConfirmRemovalModal from "../ConfirmRemovalModal";

class ClientList extends Component {
  convert_date(date){
    let s = date.split("-")
    if(s.length==3){
      return s[2]+'.'+s[1]+'.'+s[0];
    }
    return date;
  }

  render() {
    const clients = this.props.clients;
    return (
      <Table dark>
        <thead>
          <tr>
            <th>ID</th>
            <th>Last name</th>
            <th>First name</th>
            <th>CNP</th>
            <th>Birth date</th>
            <th>Registration date</th>
            <th>Points</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {!clients || clients.length <= 0 ? (
            <tr>
              <td colSpan="8" align="center">
                <b>Ops, no one here yet</b>
              </td>
            </tr>
          ) : (
            clients.map(client => (
              <tr key={client.id}>
                <td>{client.id}</td>
                <td>{client.nume}</td>
                <td>{client.prenume}</td>
                <td>{client.CNP}</td>
                <td>{client.data_nasterii = this.convert_date(client.data_nasterii)}</td>
                <td>{client.data_inregistrarii = this.convert_date(client.data_inregistrarii)}</td>
                <td>{client.puncte}</td>
                <td align="center">
                  <NewModal
                    create={false}
                    client={client}
                    resetState={this.props.resetState}
                    title="client"
                  />
                  &nbsp;&nbsp;
                  <ConfirmRemovalModal
                    id={client.id}
                    resetState={this.props.resetState}
                    table="cards"
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

export default ClientList;