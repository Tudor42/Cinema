import React from 'react';
import SideBar from './components/side_bar';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Films from './components/Film/Films.js';
import Clients from './components/Clienti/Clients';
import Bookings from './components/Rezervari/Bookings';
import FullText from './components/FullText';
import './UndoRedo.js';
import WaitModal from './components/WaitModal';

export default class App extends React.Component{


    render(){
        return(
            <div>
                <WaitModal/>
                <BrowserRouter>
                    <SideBar/>
                    <Routes>
                        <Route path='/films' exact element={<Films/>}/>
                        <Route path='/clients' exact element={<Clients/>}/>
                        <Route path='/bookings' exact element={<Bookings/>}/>
                        <Route path='/full_text' exact element={<FullText/>}/>
                    </Routes>
                </BrowserRouter>
            </div>
        )
    }
}
