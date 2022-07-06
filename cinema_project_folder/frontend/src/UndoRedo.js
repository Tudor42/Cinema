import axios from "axios";
import {API_URL} from "./constants";
import localforage from 'localforage';

var _ = require('lodash');


global.undo_redo = new class{
    undo_lst = [];
    redo_lst = [];

    async constructor_async(){

        if(sessionStorage.getItem('val') === null){
            await localforage.clear();
            sessionStorage.setItem('val', 1);
        }

        localforage.getItem('undo').then(
            value => {
                if(value !== null && typeof value !== 'undefined' ){
                    this.undo_lst = _.cloneDeep(JSON.parse(value));
                }else{
                    this.undo_lst = [];
                }
            }
        );
        localforage.getItem('redo').then(
            value => {
                if(typeof value !== 'undefined' && value !== null){
                    this.redo_lst = _.cloneDeep(JSON.parse(value));
                }else{
                    this.redo_lst = [];
                }
            }
        );

    }

    constructor(){
        this.constructor_async();
    }

    add_undo_clear_redo(operation_type, model, prev_entity, post_entity){
        // Operation types
        // 1 - one entity add
        // 2 - more than one entity add
        // 3 - one entity update
        // 4 - more than one entity update
        // 5 - one entity delete
        // 6 - more than one entity delete

        // operation      inverse
        // 1              5
        // 2              6
        // 3              3 - with changed prev and post
        // 4              4 - with changed prev in post
        // 5              1
        // 6              3
        if((Array.isArray(prev_entity) && !prev_entity.length) || (Array.isArray(post_entity) && !post_entity.length)){
            return;
        }
        if(JSON.stringify(prev_entity) !== JSON.stringify(post_entity)){
            this.redo_lst = [];
            let next_index;
            if(this.undo_lst[this.undo_lst.length - 1])
                next_index = this.undo_lst + 1;
            else
                next_index = 1;
            this.undo_lst.push(next_index);
            localforage.setItem(String(next_index), [operation_type, model, _.cloneDeep(prev_entity), _.cloneDeep(post_entity)]).then();
            localforage.setItem('undo', JSON.stringify(this.undo_lst)).then();
            localforage.setItem('redo', JSON.stringify(this.redo_lst)).then();
        }

    }

    async addEntity(table, entity){
        return await axios.post(API_URL+table+'/', entity).then(
            () => {
                return true;
            }
        ).catch(
            () => {
                return false;
            }
        )
    }

    async deleteEntity(table, entity){
        return await axios.delete(API_URL+table+'/'+entity['id']).then(
            () => {
                return true;
            }
        ).catch(
            () => {
                return false;
            }
        )
    }
    
    async updateEntity(table, postentity){
        return await axios.put(API_URL+table+'/'+postentity['id'], postentity).then(
            () => {
                return true;
            }
        ).catch(
            () => {
                return false;
            }
        )
    }

    async addEntities(table, entities){
        return await axios.post(API_URL+table+'_madd/', entities).then(
            () => {
                return true;
            }
        ).catch(
            () => {
                return false;
            }
        )
    }

    async updateEntities(table, postentities){
        return await axios.put(API_URL+table+'_mupdate/', postentities).then(
            () => {
                return true;
            }
        ).catch(
            () => {
                return false;
            }
        )
    }
    
    async deleteEntities(table, entities){
        return await axios.put(API_URL+table+'_mdelete/', entities).then(
            () => {
                return true;
            }
        ).catch(
            () => {
                return false;
            }
        )
    }

    async undo(){
        let operation_index = this.undo_lst.pop();
        
        if(typeof operation_index === 'undefined'){
            return;
        }
        
        var operation = await localforage.getItem(String(operation_index));
        let res;

        global.waitModal.turn_on();

        if(operation[0] === 1){
            res = await this.deleteEntity(operation[1], operation[3]);
        }
        if(operation[0] === 2){
            res = await this.deleteEntities(operation[1], operation[3]);
        }
        if(operation[0] === 3){
            res = await this.updateEntity(operation[1], operation[2]);
        }
        if(operation[0] === 4){
            res = await this.updateEntities(operation[1], operation[2]);
        }
        if(operation[0] === 5){
            if(operation[1]==='films'){
                res = await this.addEntity(operation[1], operation[2][0]);
                for(const id in operation[2][1]){
                    console.log(operation[2][1][id]);
                    await this.addEntity('bookings', operation[2][1][id]);
                }
            }else
                res = await this.addEntity(operation[1], operation[2]);
        }
        if(operation[0] === 6){
            res = await this.addEntities(operation[1], operation[2]);
        }
        if(res === true){
            this.redo_lst.push(operation_index);
            await localforage.setItem('undo', JSON.stringify(this.undo_lst));
            await localforage.setItem('redo', JSON.stringify(this.redo_lst));
        }

        global.waitModal.turn_off();
    }
    
    async redo(){
        let operation_index = this.redo_lst.pop();
        if(typeof operation_index === 'undefined'){
            return;
        }
        var operation = await localforage.getItem(String(operation_index));

        let res;

        global.waitModal.turn_on();
        
        if(operation[0] === 1){
            res = await this.addEntity(operation[1], operation[3]);
        }
        if(operation[0] === 2){
            res = await this.addEntities(operation[1], operation[3]);
        }
        if(operation[0] === 3){
            res = await this.updateEntity(operation[1], operation[3]);
        }
        if(operation[0] === 4){
            res = await this.updateEntities(operation[1], operation[3]);
        }
        if(operation[0] === 5){
            if(operation[1]==='films'){
                res = await this.deleteEntity(operation[1], operation[2][0]);
            }else
                res = await this.deleteEntity(operation[1], operation[2]);
        }
        if(operation[0] === 6){
            res = await this.deleteEntities(operation[1], operation[2]);
        }
        if(res === true){
            this.undo_lst.push(operation_index);
            await localforage.setItem('undo', JSON.stringify(this.undo_lst));
            await localforage.setItem('redo', JSON.stringify(this.redo_lst));
        }

        global.waitModal.turn_off();
    }
}
