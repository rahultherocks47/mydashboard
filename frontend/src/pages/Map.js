import React,{Component} from 'react';
//import './App.css';
import {Map, InfoWindow, Marker, GoogleApiWrapper} from 'google-maps-react';

export class MapContainer extends Component {
    render() {
      return (
        <Map google={this.props.google}
    
        initialCenter={{
          lat: 27.2046,
          lng: 77.4977
        }}
        zoom={15}
        onClick={this.onMapClicked}>
   
          <Marker onClick={this.onMarkerClick}
                  name={'Current location'} />
   
        </Map>
      );
    }
  }
   
  export default GoogleApiWrapper({
    apiKey: ("AIzaSyB0r8Q_VC-04p6fuXvLXFpHTitThVv-h5o")
  })(MapContainer)
  

