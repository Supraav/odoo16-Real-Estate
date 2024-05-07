/** @odoo-module **/

import { Component,useState,useRef,onMounted  } from "@odoo/owl";
import { Todo } from "../todo/todo";

export class TodoList extends Component{
    static template='client_actions.TodoList'

    addTodo(ev){
        debugger;
        if (ev.keyCode===13 && ev.target.value != ""){
            this.todoList.push({id:this.todoList.length+1,description:ev.target.value,done:false});
            ev.target.value = "";
        }    
    }

    toggleTodo(todoId) {
        const todo = this.todoList.find((todo) => todo.id === todoId);
        if (todo) {
            todo.done = !todo.done;
        }
    }

    removeTodo(todoId){
        const index = this.todoList.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            // remove the element at index from list
            this.todoList.splice(index, 1);
        }

        this.todoList.forEach((todo, index) => {
            todo.id = index + 1;
            });
    }

    setup(){
        // this.todoList = [
        //         { id: 3, description: "buy milk", done: false },
        //         { id: 4, description: "buy avocados", done: true },
        //         { id: 5, description: "buy eggs", done: false },
            
        //     ];  

        // this.newid=0;
        this.todoList=useState([]);
        const myRef = useRef('todoInput');

        onMounted(() => {
            myRef.el.focus();
          });

        console.log(this.todoList);
    }
    static components = {Todo}
}





// this.todo_list = [
//     { id: 3, description: "buy milk", done: false },
//     { id: 4, description: "buy avocados", done: true },
//     { id: 5, description: "buy eggs", done: false },

// ];  