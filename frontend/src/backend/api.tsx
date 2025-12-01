export const ENDPOINT = '/api/v1';

export type Sound = {
    identifier: string;
    description: string;
}

export type ShareResponse = {
    success: boolean;
    message_id: string;
}

export type ShareRequest = {
    user_id: number;
    identifier: string;
}

export async function getSounds(): Promise<Sound[]> {
    let response = await fetch(`${ENDPOINT}/sounds`);
    let data = await response.json();
    return data;
}

export async function requestShareSound(request: ShareRequest): Promise<ShareResponse> {
    let response = await fetch(`${ENDPOINT}/sounds/share`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
    });
    let data = await response.json();
    return data;
}
