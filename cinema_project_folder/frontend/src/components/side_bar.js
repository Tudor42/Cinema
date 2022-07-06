import React from 'react';
import {Nav, NavItem, NavLink, Navbar, NavbarBrand} from 'reactstrap';


export default class SideBar extends React.Component{
    /*
    Contains links to tables
    */ 
    render(){
        return(
            <div style={{
                top: 0, left: 0, width: '180px',
                backgroundColor: '#212529',
                height: '100vh',
                position: 'fixed', paddingTop: "20px",
            }}>
            <Navbar fixed='true' color='dark' dark='true' container='lg' style={{
                width: '180px',
                overflowx: 'hidden',
                position: 'relative',
                verticalAlign:'text-top',
                }}>
                <NavbarBrand href="/">
                    Cinema
                </NavbarBrand>
                <Nav vertical='true'>
                    
                    <NavItem>
                        <NavLink href="/films">
                            Films
                        </NavLink>
                    </NavItem>
                    <NavItem>
                        <NavLink href="/bookings">
                            Bookings
                        </NavLink>
                    </NavItem>
                    <NavItem>
                        <NavLink href="/clients">
                            Clients
                        </NavLink>
                    </NavItem>
                    <br/>
                    <hr/>
                    <NavItem>
                        <NavLink href="/full_text">
                            Full Text Search
                        </NavLink>
                    </NavItem>
                    <br/>
                </Nav>
                <NavItem
                    style={{
                        position: 'relative',
                        bottom: '-20px'
                    }}
                >
                    <NavLink href="/docs">
                        Documentation
                    </NavLink>
                </NavItem>
            </Navbar>
            </div>
        )
    }
}