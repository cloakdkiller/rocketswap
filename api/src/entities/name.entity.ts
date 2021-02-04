import { IKvp } from "src/types/misc.types";
import { getVal } from "../utils";
import { config } from "../config";
import {
	Entity,
	Column,
	BaseEntity,
	PrimaryColumn
} from "typeorm";

/** An instance of this entity is created after each action on the AMM that changes the price variable. */

@Entity()
export class NameEntity extends BaseEntity {
	@PrimaryColumn()
	vk: string;

	@Column()
	name: string;
}

export const setName = async (state: IKvp[]) => {
	console.log('SAVE NAME ACTIVATED')
	const key_to_name = state.find(
		(kvp) =>
			kvp.key.split(":")[0] === `${config.identityContract}.key_to_name`
	);
	const name_to_key = state.find(
		(kvp) =>
			kvp.key.split(":")[0] ===
				`${config.identityContract}.name_to_key` && kvp.value
	);
	console.log(name_to_key, key_to_name)
	if (key_to_name && name_to_key) {
		const vk = name_to_key.value;
		const name = key_to_name.value;

		let entity;
		entity = await NameEntity.findOne(vk);
		if (!entity) {
			entity = new NameEntity();
			entity.vk = vk;
		}
		entity.name = name;
		await entity.save();
	}
};