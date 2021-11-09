import React, { useCallback, useState } from "react";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, InputGroup, Navbar, NavbarBrand, Input, Card, CardBody,  CardTitle, CardImg, Row, Col, InputGroupText, Container } from 'reactstrap';
import Dropzone from 'react-dropzone';
import { BiDownload, BiWrench } from "react-icons/bi";
function App() {
  const [image, setImage]=useState(null)
  const [compressRate, setCompressRate]=useState(null)

  const handleDrop = acceptedFiles => {
    setImage(URL.createObjectURL(acceptedFiles[0]));
  };
  var compRate;
  function compressFunc(){
    compRate=document.getElementById("compRateInput").value;
    document.getElementById("printCompRate").innerHTML = compRate;
  }

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
          <Dropzone accept='image/*' onDrop={handleDrop} className="contDrop">
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
          <Button onClick={compressFunc} size='lg' style={{margin:'20px'}}><BiWrench/>  Compress</Button>
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
                    />
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
