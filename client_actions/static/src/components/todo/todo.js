/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Todo extends Component{
    static template='client_actions.Todo'
    
    static props = {
        id: { type: Number },
        description: { type: String },
        done: { type: Boolean },
        // toggleState: { type: Function },
        // removeTodo: { type: Function },
    };
}