import React, { useCallback, useEffect, useState } from "react";
import ReactDOM from "react-dom";
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById("root"));

const EDisease = {
    NONE: 0,
    DIABETE: 1,
    OBESITY: 2,
    CELIAC: 3,
    LACTOSE_INTOLERANCE: 4,
    HIGH_BLOOD_PRESSURE: 5,
    KIDNEY_DISEASE: 6,
    GOUT: 7,
    HEART_DISEASE: 8,
    SIZE: 9
};
Object.freeze(EDisease);

const EAllergy = {
    NONE: 0,
    EGGS: 1,
    SESAME: 2,
    MILK: 3,
    BEANS: 4,
    PEANUT: 5,
    FRUITS_AND_VEGITABLES: 6,
    NUTS: 7,
    SEA_FOODS: 8,
    WHEAT: 9,
    SIZE: 10
};
Object.freeze(EAllergy);

const EReligion = {
    NONE: 0,
    ISLAM: 1,
    JUDAISM: 2,
    BUDDHISM: 3,
    SEVENTH_DAY_ADVENTIST_CHURCH: 4,
    SIKHISH: 5,
    SIZE: 6
};
Object.freeze(EReligion);

function AddDiseaseOptions() {
    return <>
        <option value={EDisease.NONE}>없음</option>
        <option value={EDisease.DIABETE}>당뇨</option>
        <option value={EDisease.OBESITY}>비만</option>
        <option value={EDisease.CELIAC}>셀리악(Celiac)</option>
        <option value={EDisease.LACTOSE_INTOLERANCE}>유당불내증</option>
        <option value={EDisease.HIGH_BLOOD_PRESSURE}>고혈압</option>
        <option value={EDisease.KIDNEY_DISEASE}>신장 질환</option>
        <option value={EDisease.GOUT}>통풍</option>
        <option value={EDisease.HEART_DISEASE}>심장 질환</option>
    </>;
}

function AddAllergyOptions() {
    return <>
        <option value={EAllergy.NONE}>없음</option>
        <option value={EAllergy.EGGS}>알류</option>
        <option value={EAllergy.SESAME}>참깨</option>
        <option value={EAllergy.MILK}>우유</option>
        <option value={EAllergy.BEANS}>콩(대두)</option>
        <option value={EAllergy.PEANUT}>땅콩</option>
        <option value={EAllergy.FRUITS_AND_VEGITABLES}>과일 및 채소</option>
        <option value={EAllergy.NUTS}>견과류</option>
        <option value={EAllergy.SEA_FOODS}>해산물</option>
        <option value={EAllergy.WHEAT}>밀</option>
    </>;
}

function AddReligionOptions() {
    return <>
        <option value={EReligion.NONE}>없음</option>
        <option value={EReligion.ISLAM}>이슬람교</option>
        <option value={EReligion.JUDAISM}>유대교</option>
        <option value={EReligion.BUDDHISM}>불교</option>
        <option value={EReligion.SEVENTH_DAY_ADVENTIST_CHURCH}>제칠일안식일예수재림교</option>
        <option value={EReligion.SIKHISH}>시크교</option>
    </>;
}

function CreateUserDataForm() {
    const [State, SetState] = useState({
        userLocation: {
            latitude: 0.0,
            longitude: 0.0
        },
        userDisease: EDisease.NONE,
        userAllergy: EAllergy.NONE,
        userReligion: EReligion.NONE,
        userVegan: false
    })

    function getCurrentPositionPromise() {
        return new Promise( (resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                position => resolve(position),
                error => reject(error)
            )
        })
    }

    const AGetGeolocation = async () => {
        var position = await getCurrentPositionPromise();
        //window.alert(position.coords.latitude + ' ' + position.coords.longitude);
        document.getElementById("FoodCards").innerHTML=position.coords.latitude + ', ' + position.coords.longitude;
        return {latitude: position.coords.latitude, longitude: position.coords.longitude};
    }

    const HandleSubmit = async (e) => {
        e.preventDefault();
        var location = await AGetGeolocation();
        var updatedState = {
            ...State,
            userLocation: location,
        };

        SetState(updatedState);

        //TODO - request

        fetch('/api',
        {
            method : "POST",
            headers : {
                "Content-Type" : "application/json; charset=utf-8"
            },
            body : JSON.stringify(updatedState)
        })
        .then(res => res.json())
        .then(res => {
            console.log(res);
            document.getElementById("FoodCards").innerHTML=JSON.stringify(res, null, 2);
        })

        return;
    }

    // useEffect(() => {
    //     alert(JSON.stringify(State, null, 2));
    // }, [State])

    const HandleSelect = async (e) => {
        var updatedState = {
            ...State,
            [e.target.id]: e.target.value
        };

        SetState(updatedState);
    }

    return (
    <div className="container">
        <form id="userData" className="p-2 bg-secondary text-center" onSubmit={HandleSubmit}>
        <div className="row my-2">
            <div className="col">
                <h3>질병여부</h3>
                <select id="userDisease" onChange={HandleSelect}>
                    <AddDiseaseOptions />
                </select>
            </div>
            <div className="col">
                <h3>알러지 여부</h3>
                <select id="userAllergy" onChange={HandleSelect}>
                    <AddAllergyOptions />
                </select>
            </div>
            <div className="col">
                <h3>종교 여부</h3>
                <select id="userReligion" onChange={HandleSelect}>
                    <AddReligionOptions />
                </select>
            </div>
            <div className="col">
                <h3>비건 여부</h3>
                <select id="userVegan" onChange={HandleSelect}>
                <option value={false}>아니오</option>
                <option value={true}>예</option>
                </select>
            </div>
        </div>
        <div className="row justify-content-center">
            <button type="submit" className="btn btn-primary w-25">추천받기</button>
        </div>
        </form>
    </div> );
}

function HandleFoodCards() {
    return <>
        <div id="FoodCards" className="vw-100 p-3 bg-info">test</div>
    </>;
}

function RenderRoot() {
    return <>
        <CreateUserDataForm />
        <HandleFoodCards />
    </>;
}

root.render(<RenderRoot />);