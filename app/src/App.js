import React, { useCallback, useState } from "react";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, InputGroup, Navbar, NavbarBrand, Input, Card, CardBody,  CardTitle, CardImg, Row, Col, InputGroupText, Container } from 'reactstrap';
import Dropzone from 'react-dropzone';

function App() {
  const [image, setImage]=useState(null)
  const [compressRate, setCompressRate]=useState(null)

  const handleDrop = acceptedFiles => {
    setImage(URL.createObjectURL(acceptedFiles[0]));
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
        <div style={{margin:'50px'}}>
          <Container className="contDrop" >
            <Dropzone accept='image/*' onDrop={handleDrop}>
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
            <Input type="number"/>
            <InputGroupText>%</InputGroupText>
          </InputGroup>
          <Button size='lg' style={{margin:'20px'}}>Compress</Button>
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
