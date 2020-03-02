import React from 'react';
import { Link } from 'react-router-dom';

import { faPhoneAlt, faBackspace } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import styles from './Keyboard.css';

const Keyboard = ({ action, remove, call }) => {
    return(
        <div>
            <div>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={ () => action(1)}><span>1</span></button>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={ () => action(2)}><span>2</span></button>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={ () => action(3)}><span>3</span></button>
            </div>
            <div>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={ () => action(4)}><span>4</span></button>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={ () => action(5)}><span>5</span></button>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={ () => action(6)}><span>6</span></button>
            </div>                    
            <div>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={ () => action(7)}><span>7</span></button>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={ () => action(8)}><span>8</span></button>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={ () => action(9)}><span>9</span></button>
            </div>                    
            <div>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={ () => action("+")}><span>+</span></button>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={ () => action(0)}><span>0</span></button>
                <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick= { () => remove()}><span><FontAwesomeIcon icon={faBackspace} /></span></button>
            </div>                    
            <div>
                <Link to="/Calling">
                    <button className={styles.Button} style={{verticalAlign: 'middle'}} onClick={() => call()}><span><FontAwesomeIcon icon={faPhoneAlt} /></span></button>
                </Link>
            </div>
        </div>
    )
}

export default Keyboard;