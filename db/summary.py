def generate_summary(request: SummaryBase, db: Session = Depends(get_db)):
    
    title_category = generate_metadata(request.path)
    print(title_category)
    
    newJsonMeta = json.loads(title_category)
    
    message = generate_summaries(request.path)
    
    newJson = json.loads(message)
    
    print(newJson)
    
    new_summary = DbSummary(
        title = newJsonMeta["title"],
        ownerId = 1,
        #Flash cards
        category_id = newJsonMeta["category"],
        isPublic = request.isPublic
    )
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    
    host = "https://229b-34-80-43-24.ngrok-free.app/"
    generate_image_url = f"{host}/generateImage"

    for json_item in newJson:
        json_request = {"prompt": f"Generate a realistic image that can acompany a flashcard called {json_item['title']}. The image should be clear and it has educational purposes"}
        generate_image_response = requests.post(generate_image_url, json=json_request)
        new_flash = FlashCardBase(
            title=json_item['title'],
            content=json_item['content'],
            imagePath=f"{generate_image_response.content.decode('utf-8')}",
            summaryId=new_summary.summaryId
        )
        create_flash_card(new_flash, db)
    
    return new_summary