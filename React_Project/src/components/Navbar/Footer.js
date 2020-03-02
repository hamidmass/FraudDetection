import React from 'react';
import './Navbar.css';

 /* Footer.jsx */
function footer() {
    const styles = {
      footer: {
        position: 'absolute',
        bottom: 0,
        width: '100%',
        marginTop: '1rem',
        display:'flex',
        flexDirection:'column',
        justifyContent:'center',
        alignItems:'center',
        color: 'black',
      },
      
      text: {
        padding: '0.5rem',
        fontWeight: 'bold'
      }
    }  
    
    return (
      <div style={styles.footer}>
        <div style={styles.text}>GVO &copy; 2019</div>
      </div>
    )
}

export default footer;