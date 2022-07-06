import React, { Component, Fragment } from "react";
import { Button, Modal, ModalHeader, ModalBody } from "reactstrap";
import NewFilmForm from "./Film/NewFilmForm";
import NewClientForm from "./Clienti/NewClientForm";
import NewBookingForm from "./Rezervari/NewBookingForm"

class NewModal extends Component {
    /*
        Modal that renders modals for editing or updating objects
    */ 
    state = {
        modal: false
    };

    toggle = () => {
        this.setState(previous => ({
            modal: !previous.modal
        }));
    };

    render() {
        const create = this.props.create;

        var title = "Editing "+this.props.title;
        var button = <Button onClick={this.toggle}>Edit</Button>;
        if (create) {
            title = "Creating New "+this.props.title;

            button = (
                <Button
                    color="primary"
                    className="float-right"
                    onClick={this.toggle}
                    style={{ minWidth: "200px" }}
                >
                    Create New
                </Button>
            );
        }

        return (
            <Fragment>
                {button}
                <Modal isOpen={this.state.modal} toggle={this.toggle}>
                    <ModalHeader toggle={this.toggle}>{title}</ModalHeader>

                    <ModalBody>
                        {this.props.title==="film"?
                        (<NewFilmForm
                            resetState={this.props.resetState}
                            toggle={this.toggle}
                            film={this.props.film}
                        />): this.props.title==="client"?(<NewClientForm
                            resetState={this.props.resetState}
                            toggle={this.toggle}
                            client={this.props.client}
                        />):(
                            <NewBookingForm
                                resetState={this.props.resetState}
                                toggle={this.toggle}
                                booking={this.props.booking}
                            />
                        )}
                    </ModalBody>
                </Modal>
            </Fragment>
        );
    }
}

export default NewModal;