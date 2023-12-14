from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

_model = BartForConditionalGeneration.from_pretrained('./Service/best_model')


# _device = torch.device("cuda" if torch.cuda_is_available() else "cpu")
# _model.to(_device)
def inference_store_name(query: str) -> str:
    query = query.replace('\n', '')

    tokenizer = PreTrainedTokenizerFast.from_pretrained("gogamza/kobart-base-v2")

    input_ids = tokenizer.encode(query, return_tensors='pt')
    # input_ids = input_ids.to(device)

    output = _model.generate(input_ids,
                             eos_token_id=1,
                             max_length=16,
                             num_beams=5,
                             no_repeat_ngram_size=2,
                             early_stopping=True)

    output = tokenizer.decode(output[0])
    processed_output = postprocess(output)

    return processed_output


def postprocess(output: str) -> str:
    output = output.replace('</s>', '')
    output = output.split('(')[0]
    output = output.strip()
    return output
