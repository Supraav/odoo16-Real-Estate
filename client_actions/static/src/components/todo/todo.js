/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Todo extends Component{
    static template='client_actions.Todo'

    onClick(){
        this.props.toggleState(this.props.ids);
    }
    onRemove(){
        this.props.removeTodo(this.props.ids);
    }
    
    static props = {
        ids: { type: Number },
        description: { type: String },
        done: { type: Boolean },
        toggleState: { type: Function },
        removeTodo: { type: Function },
    };
}