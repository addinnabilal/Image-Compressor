import React, { useState } from "react";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, InputGroup, Navbar, NavbarBrand, Input, Card, CardBody,  CardTitle, CardImg, Row, Col, InputGroupText, Container } from 'reactstrap';
import Dropzone from 'react-dropzone';

function App() {
  const [image, setImage]=useState(null);
  const [compressRate, setCompressRate]=useState(null);
  // const handleDrop = acceptedFiles => {
  //   // console.log(acceptedFiles)
  //   setImage(URL.createObjectURL(acceptedFiles[0]));
  // };
  const handleChange = function(e){
    console.log("k = " + e.target.value);
    setCompressRate(e.target.value);
  }

  const handleUploadImage = function(ev){
    // ev.preventDefault();
    setImage(ev[0]);
    const data = new FormData();
    // console.log(compressRate);
    // console.log(ev)
    data.append('file', image);
    data.append('k', compressRate);

    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      console.log(response)
    });}
    
  const handleCompress = function(){
    console.log(image);
    fetch('http://localhost:5000/download/' + image.name, {
    method: 'GET',
  }).then((res) => {
    console.log("Get download url success.");
    setImage(res.url)
    // this.setState({imageURL:res.url})});
  })};
   

  return (
    <div className="App">
      <header>
        <Navbar style={{backgroundColor:'#864879'}} dark>
          <NavbarBrand href="/">
            Image Compressor
          </NavbarBrand>
        </Navbar>
        <div>
          <h1 style={{color:'#E9A6A6', marginTop:'30px'}}>Compress Your Image Here!</h1>
        </div>
      </header>
      <body>
        <div style={{margin:'50px'}}>
          <Container className="contDrop" >
            <Dropzone accept='image/*' onDrop={handleUploadImage}>
              {({ getRootProps, getInputProps }) => (
                <div {...getRootProps({ className: "dropzone" })}>
                  <input {...getInputProps()} />
                  <p style={{color:'white'}}>Drag and drop files, or click to select files</p>
                </div>
              )}
            </Dropzone>
          </Container>
          <InputGroup size='sm' style={{marginTop:'20px'}}>
            <InputGroupText>Compression Rate</InputGroupText>
            <Input type="number" onChange={handleChange}/>
            <InputGroupText>%</InputGroupText>
          </InputGroup>
          <Button size='lg' onClick={handleCompress} style={{margin:'20px'}}>Compress</Button>
          <Row>
            <Col>
              <Card>
                <CardBody>
                  <CardTitle>
                    Before
                  </CardTitle>
                  <CardImg
                  src={image}/>
                </CardBody>
              </Card>
            </Col>
            <Col>
              <Card>
                <CardBody>
                  <CardTitle>
                    After
                  </CardTitle>
                  <CardImg>

                  </CardImg>
                </CardBody>
              </Card>
            </Col>
          </Row>
        </div>
        
      </body>
    </div>
  );
}

export default App;
