import React, { Component } from 'react';

import './Navbar.css';
import Footer from './Footer';
import Menu from './Menu';
import MenuButton from './MenuButton';
import MenuItem from './MenuItem';

class Navbar extends Component {
    constructor(props){
      super(props);
      this.state={
        menuOpen:false,
      }
    }
    
    handleMenuClick() {
      this.setState({menuOpen:!this.state.menuOpen});
    }
    
    handleLinkClick() {
      this.setState({menuOpen: false});
    }
    
    render(){
      const styles= 
        {
          container:{
            position: 'absolute',
            top: 0,
            left: 0,
            zIndex: '99',
            opacity: 0.9,
            display:'flex',
            alignItems:'center',
            background: 'black',
            width: '100%',
            color: '#66FCF1',
            fontFamily:'Lobster',
            fontSize:'15px'
          },
          logo: {
            margin: '0 auto',
          },
        }
      const menu = ['Services','Pricing','Why Acintya','About Us','Contact Us'];
      const menuItems = menu.map((val,index)=>{
        return (
          <MenuItem 
            key={index} 
            delay={`${index * 0.1}s`}
            onClick={()=>{this.handleLinkClick();}}>{val}</MenuItem>);
      });
      
      return(
        <div>
          <div style={styles.container}>
            <MenuButton open={this.state.menuOpen} onClick={()=>this.handleMenuClick()} color='#66FCF1'/>
            <div style={styles.logo}>Global Virtual Office</div>
          </div>
          <Menu open={this.state.menuOpen}>
            {menuItems}
          </Menu>
          <div>
            <Footer />
          </div>
        </div>
      )
    }
  }

export default Navbar;
  
  
