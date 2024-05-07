/** @odoo-module **/

import { Component,useState  } from "@odoo/owl";
import { Todo } from "../todo/todo";

export class TodoList extends Component{
    static template='client_actions.TodoList'

    addTodo(ev){
        if (ev.keyCode===13 && ev.target.value != ""){
            this.todoList.push({id:this.newid++,description:ev.target.value,done:false});
            ev.target.value = "";
        }    
    }

    setup(){
        // this.todoList = [
        //         { id: 3, description: "buy milk", done: false },
        //         { id: 4, description: "buy avocados", done: true },
        //         { id: 5, description: "buy eggs", done: false },
            
        //     ];  

        this.newid=0;
        this.todoList=useState([]);
        console.log(this.todoList);
    }
    static components = {Todo}
}





// this.todo_list = [
//     { id: 3, description: "buy milk", done: false },
//     { id: 4, description: "buy avocados", done: true },
//     { id: 5, description: "buy eggs", done: false },

// ];  