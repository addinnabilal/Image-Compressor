import React, { useState } from "react";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, InputGroup, Navbar, NavbarBrand, Input, Card, CardBody,  CardTitle, CardImg, Row, Col, InputGroupText, Container } from 'reactstrap';
import Dropzone from 'react-dropzone';
import { BiDownload, BiWrench } from "react-icons/bi";
function App() {
  const [image, setImage]=useState(null);
  const [compressRate, setCompressRate]=useState(null);
  const [imageName, setImageName]=useState(null);
  const [compImage, setCompImage]=useState(null);
  // const handleDrop = acceptedFiles => {
  //   // console.log(acceptedFiles)
  //   setImage(URL.createObjectURL(acceptedFiles[0]));
  // };
  //const handleChange = function(e){
  //  console.log("k = " + e.target.value);
  //  setCompressRate(e.target.value);
  //} GAS ini gua pindahin ke func compress ya sekalian

  const handleUploadImage = function(ev){
    // ev.preventDefault();
    setImageName(ev[0].name);
    setImage(URL.createObjectURL(ev[0]));
    const data = new FormData();
    console.log(imageName);
    data.append('file', ev[0]);
    data.append('k', compressRate);
    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      console.log(response)
    });}
    
  var compRate;
  const handleCompress = function(){
    fetch('http://localhost:5000/download/' + imageName, {
    method: 'GET',
  }).then((res) => {
    console.log("Get download url success.");
    console.log(res.url);
    setCompImage(res.url);
  })
    compRate=document.getElementById("compRateInput").value;
    document.getElementById("printCompRate").innerHTML = compRate;
    setCompressRate(compRate);
};
   
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
        <div style={{margin:'100px', marginTop:'10px'}}>
          <Dropzone accept='image/*' onDrop={handleUploadImage} className="contDrop">
            {({ getRootProps, getInputProps }) => (
              <div {...getRootProps({ className: "dropzone" })}>
                <input {...getInputProps()} />
                <p style={{color:'white'}}>Drag and drop files, or click to select files</p>
              </div>
            )}
          </Dropzone>
          <InputGroup size='sm' style={{marginTop:'20px'}}>
            <InputGroupText>Compression Rate</InputGroupText>
            <Input type="number" id="compRateInput"/>
            <InputGroupText>%</InputGroupText>
          </InputGroup>
          <Button onClick={handleCompress} size='lg' style={{margin:'20px'}}><BiWrench/>  Compress</Button>
          <Row>
            <Col>
              <Card>
                <CardBody>
                  <CardTitle>
                    Before
                  </CardTitle>
                  <Container className='imgCont'>
                    <CardImg
                    src={image} style={{maxHeight:'100%',objectFit:'contain', alignItems:'center', justifyContent:'content'}}/>
                  </Container>
                </CardBody>
              </Card>
            </Col>
            <Col>
              <Card>
                <CardBody>
                  <CardTitle>
                    After
                  </CardTitle>
                  <Container className='imgCont'>
                  <CardImg
                    src={compImage} style={{maxHeight:'100%',objectFit:'contain', alignItems:'center', justifyContent:'content'}}/>
                  </Container>
                </CardBody>
              </Card>
            </Col>
          </Row>
          <div style={{marginTop:'10px'}}>
              <Container>
                <p style={{color:'white'}}>Image pixel difference percentage <span id="printCompRate"></span>%</p>
              </Container>
              <Container>
                <p style={{color:'white'}}>Image compression time<span id="printCompTime"></span>%</p>
              </Container>
              <Container>
                <Button><BiDownload/>  Download</Button>
              </Container>
          </div>
        </div>
      </body>
    </div>
  );
}

export default App;
