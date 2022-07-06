import React, { Component } from "react";
import { Table } from "reactstrap";
import NewModal from "../NewModal";
import ConfirmRemovalModal from "../ConfirmRemovalModal";

class BookingList extends Component {
  convert_date(date){
    if(date){
      let s = date.split("-")
      if(s.length==3){
        return s[2]+'.'+s[1]+'.'+s[0];
      }
    }
    return date;
  }

  render() {
    const bookings = this.props.bookings;
    return (
      <Table dark>
        <thead>
          <tr>
            <th>ID</th>
            <th>Film</th>
            <th>Client</th>
            <th>Date</th>
            <th>Hour</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {!bookings || bookings.length <= 0 ? (
            <tr>
              <td colSpan="6" align="center">
                <b>Ops, no one here yet</b>
              </td>
            </tr>
          ) : (
            bookings.map(booking => (
              <tr key={booking.id}>
                <td>{booking.id}</td>
                <td>{booking.str_film.slice(0, booking.str_film.lastIndexOf(' '))}</td>
                <td>{booking.str_client? 
                booking.str_client.slice(0, booking.str_client.lastIndexOf(' ')):
                booking.str_client}</td>
                <td>{booking.data = this.convert_date(booking.data)}</td>
                <td>{booking.ora = booking.ora.slice(0, 5)}</td>
                <td align="center">
                  <NewModal
                    create={false}
                    booking={booking}
                    resetState={this.props.resetState}
                    title="booking"
                  />
                  &nbsp;&nbsp;
                  <ConfirmRemovalModal
                    id={booking.id}
                    resetState={this.props.resetState}
                    table="bookings"
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

export default BookingList;