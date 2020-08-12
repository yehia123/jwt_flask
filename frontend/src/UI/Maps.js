import React, { Component } from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";
import { Map, GoogleApiWrapper } from 'google-maps-react';

const mapStyles = {
    width: '100%',
    height: '100%'
};

export class MapContainer extends Component {
    render() {
        return (
            <React.Fragment>
                <Map
                    google={this.props.google}
                    zoom={8}
                    style={mapStyles}
                    initialCenter={{ lat: 47.444, lng: -122.176 }}
                />
            </React.Fragment>
        );
    }
}


export default GoogleApiWrapper({
    apiKey: 'AIzaSyB7bg2vvcyBeZSyyBie_yJIbxPEfBGz320'
})(MapContainer);