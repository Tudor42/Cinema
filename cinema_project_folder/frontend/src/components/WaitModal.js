import React, { Component, Fragment } from "react";
import { Modal, ModalHeader, ModalBody } from "reactstrap";

global.waitModal = null;

export default class WaitModal extends Component{
    /*
        This modal is created to block tab
        if waiting for a request response

        Used everywhere where request changes database state
    */ 

    wait = false;
    
    componentDidMount(){
        global.waitModal = this; // assign component to a global variable
        // so it could be accessed by all components
        this.wait = false;
    }

    turn_on(){
        // Show the modal
        this.wait = true;
        this.forceUpdate();
    }

    turn_off(){
        // Hide the modal
        this.wait = false;
        this.forceUpdate();
    }

    render(){
        return(
            <Fragment>
                <Modal isOpen={this.wait}>
                    <ModalHeader>Please wait</ModalHeader>
                    <ModalBody>
                        Operation in progres
                    </ModalBody>
                </Modal>
            </Fragment>
        )
    }
}