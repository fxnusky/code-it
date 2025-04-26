'use client';
import { PlayerRanking } from "../../../components/player_ranking";

export default function Test() {
    let func = () => {

    }
    let ranking: [string, number][] = [["nickname", 100000], ["nickname", 34], ["nickname", 19], ["nickname", 18], ["nickname", 17], ["nickname", 16], ["nickname", 15], ["nickname", 14], ["nickname", 13], ["nickname", 12], ["nickname", 11], ["nickname", 10], ["nickname", 9], ["nickname", 8], ["nickname", 7], ["nickname", 6], ["nickname", 5], ["nickname", 4]]
    
    return(
        <PlayerRanking points={20} nickname={"guille"}></PlayerRanking>
    )
}
