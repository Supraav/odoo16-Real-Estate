/** @odoo-module **/

import { Component,useSubEnv } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class NavCard extends Component{}

NavCard.template="estate.Navcard";

NavCard.props={
    slots:{
        type:Object,
        shape:{
            default:Object,
            title:{type:Object,optional:true,}
        },
    },
};