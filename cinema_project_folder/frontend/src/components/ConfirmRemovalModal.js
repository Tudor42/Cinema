import React, { Component, Fragment } from "react";
import { Modal, ModalHeader, Button, ModalFooter } from "reactstrap";
import "../UndoRedo.js";
import axios from "axios";

import "../UndoRedo"

import { API_URL } from "../constants";

class ConfirmRemovalModal extends Component {
  state = {
    modal: false,
  };

  toggle = () => {
    this.setState(previous => ({
      modal: !previous.modal
    }));
  };

  deleteObject = id => {
    global.waitModal.turn_on();
    axios.delete(API_URL + this.props.table +"/"+ id).then(res => {
      global.undo_redo.add_undo_clear_redo(5, this.props.table, res.data, null);
      global.waitModal.turn_off();
      this.props.resetState();
      this.toggle();
    })
    .catch(()=>global.waitModal.turn_off());
  };

  render() {
    return (
      <Fragment>
        <Button color="danger" onClick={() => this.toggle()}>
          Remove
        </Button>
        <Modal isOpen={this.state.modal} toggle={this.toggle}>
          <ModalHeader toggle={this.toggle}>
            Do you really wanna delete the {this.props.table}?
          </ModalHeader>

          <ModalFooter>
            <Button type="button" onClick={() => this.toggle()}>
              Cancel
            </Button>
            <Button
              type="button"
              color="primary"
              onClick={() => this.deleteObject(this.props.id)}
            >
              Yes
            </Button>
          </ModalFooter>
        </Modal>
      </Fragment>
    );
  }
}

export default ConfirmRemovalModal;