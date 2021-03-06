import React, { useState } from "react";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, InputGroup, Navbar, NavbarBrand, Input, Card, CardBody,  CardTitle, CardImg, Row, Col, InputGroupText, Container } from 'reactstrap';
import Dropzone from 'react-dropzone';
import { BiDownload, BiWrench } from "react-icons/bi";
function App() {
  const [image, setImage]=useState(null);
  const [imageName, setImageName]=useState(null);
  const [compImage, setCompImage]=useState(null);
  const [currentK, setCurrentK]=useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const handleChange = function(e){
   setCurrentK(e.target.value)
  }

  const handleUploadImage = function(ev){
    // ev.preventDefault();
    setImageName(ev[0].name);
    setImage(URL.createObjectURL(ev[0]));
    const data = new FormData();
    data.append('file', ev[0]);
    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: data,
    });
    // .then((response) => {
    //   response.json();
    // }).then(data =>{
    //   // console.log(data)
    // });  
  }
  


  // TODO: Gambar belom berubah kalo sama
  const handleCompress = function(){
    setIsLoading(true);
    console.log(currentK)
    fetch('http://localhost:5000/compress/' + currentK + "_" + imageName, {
    method: 'GET',
  }).then((res) => {
    console.log("Compress success.")
    setCompImage('http://localhost:5000/download/' + currentK + "_" + imageName);
    fetch('http://localhost:5000/data')
    .then(res => res.json()).then(data => {
      console.log(data)
      document.getElementById("printCompRate").innerText = data.diff;
      document.getElementById("printCompTime").innerText = data.time;
    })
    setIsLoading(false);
  })

};
   
  const downloadFile = () => {
    window.location.href = compImage;
  }

  return (
    <div className="App">
      <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" />
      </head>
      <header>
        <Navbar style={{backgroundColor:'#864879'}} dark >
          <NavbarBrand href="/" className="nvbrand" style={{fontSize:"medium"}}>
            Image Compressor
          </NavbarBrand>
        </Navbar>
        <div>
          <h1 style={{color:'#E9A6A6', marginTop:'30px', fontSize:"35px"}}>Compress Your Image Here!</h1>
        </div>
      </header>
      <body>
        <div style={{margin:'100px', marginTop:'10px'}}>
          <Dropzone accept='image/*' onDrop={handleUploadImage} className="contDrop">
            {({ getRootProps, getInputProps }) => (
              <div {...getRootProps({ className: "dropzone" })}>
                <input {...getInputProps()} />
                <p>Drag and drop files, or click to select files</p>
              </div>
            )}
          </Dropzone>
          <InputGroup size="lg" style={{marginTop:'20px'}}>
            <InputGroupText >Compression Rate</InputGroupText>
            <Input type="number" id="compRateInput" onChange={handleChange}/>
          </InputGroup>
          <Button onClick={handleCompress} size='lg' style={{margin:'20px'}}><BiWrench/>  Compress</Button>
          <Row>
            <Col>
              <Card>
                <CardBody>
                  <CardTitle style={{fontSize:"medium"}}>
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
                  <CardTitle style={{fontSize:"medium"}}>
                    After
                  </CardTitle>
                  <Container className='imgCont'>
                  <CardImg
                    id="compImg" src={compImage} style={{maxHeight:'100%',objectFit:'contain', alignItems:'center', justifyContent:'content'}}/>
                  </Container>
                </CardBody>
              </Card>
            </Col>
          </Row>
          {isLoading ? (
              <div style={{marginTop:'10px'}}>
              <Container>
              <p>Loading... Please wait.</p>
              </Container>
              </div>
            ) : 
          <div style={{marginTop:'10px'}}>
              <Container>
                <p>Image pixel difference percentage: <span id="printCompRate"></span>%</p>
              </Container>
              <Container>
                <p>Image compression time: <span id="printCompTime"></span> s</p>
              </Container>
              <Container>
                <Button size="lg" onClick={downloadFile}><BiDownload/>  Download</Button>
              </Container>
          </div>}
        </div>
      </body>
    </div>
  );
}

export default App;
