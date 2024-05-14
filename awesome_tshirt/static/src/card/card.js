/** @odoo-module **/

import { Component,useSubEnv } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class Card extends Component{}

Card.template="awesome_tshirt.Card";

Card.props={
    slots:{
        type:Object,
        shape:{
            default:Object,
            title:{type:Object,optional:true,}
        },
    },
    className: {
        type: String,
        optional: true,
    },
};