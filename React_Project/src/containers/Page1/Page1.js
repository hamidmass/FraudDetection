import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import styles from './Page1.css';

class Page1 extends Component {

    render() {
    return (
            <div className={styles.buttons}>
                <div>
                    <Link to="/Call">
                        <button className={[styles.btn, styles.drawBorder].join(' ')}>Call</button>
                    </Link>
                    <button className={[styles.btn, styles.drawBorder].join(' ')}>Fax</button>
                </div>
                <div>
                    <button className={[styles.btn, styles.drawBorder].join(' ')}>SMS</button>
                    <button className={[styles.btn, styles.drawBorder].join(' ')}>VideoConference</button>
                </div>
            </div>
    )};
}

export default Page1;